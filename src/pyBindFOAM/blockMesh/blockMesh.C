#include "blockMesh.H"
#include "pyBindFOAM/fvCFDWrapper/fvCFDWrapper.H"
#include <string>
#include <vector>

blockMesh::blockMesh(const fvCFDWrapper& foamCase) : foamCase_(foamCase){}

blockMesh::~blockMesh()
{
    Foam::Info << "blockMesh destructor" << Foam::endl;
}

void blockMesh::generateMesh()
{

    argList::addNote
    (
        "Block mesh generator.\n"
        "  The ordering of vertex and face labels within a block as shown "
        "below.\n"
        "  For the local vertex numbering in the sequence 0 to 7:\n"
        "    Faces 0, 1 (x-direction) are left, right.\n"
        "    Faces 2, 3 (y-direction) are front, back.\n"
        "    Faces 4, 5 (z-direction) are bottom, top.\n"
        "\n"
        "                        7 ---- 6\n"
        "                 f5     |\\     |\\     f3\n"
        "                 |      | 4 ---- 5     \\\n"
        "                 |      3 |--- 2 |      \\\n"
        "                 |       \\|     \\|      f2\n"
        "                 f4       0 ---- 1\n"
        "    Y  Z\n"
        "     \\ |                f0 ------ f1\n"
        "      \\|\n"
        "       O--- X\n"
    );

    argList::noParallel();

    argList::validOptions.insert
    (
        "blockTopology",
        "Write block edges and centres as obj files and exit"
    );
    argList::validOptions.insert
    (
        "dict",
        "Alternative location for the blockMeshDict"
    );

#   include "addRegionOption.H"

    timeSelector::addOptions();

    std::vector<std::string> arguments = {"null"};

    std::vector<char*> argv_;
    for (const auto& arg : arguments)
        argv_.push_back((char*)arg.data());
    argv_.push_back(nullptr);

    int argc = argv_.size() - 1;
    char** argv = argv_.data();

#include "setRootCase.H"

    Foam::Info << "Create time\n" << Foam::endl;

    const Foam::fileName rootPath = ".";
    const Foam::fileName caseName = ".";

    Foam::Time runTime(foamCase_.getControlDict(), Foam::fileName("."), Foam::fileName("."), 
            Foam::word("system"), Foam::word("constant"), false);

    instantList timeDirs = timeSelector::select0(runTime, args);

    word regionName = polyMesh::defaultRegion;
    word regionPath;

    if (args.optionFound("region"))
    {
        Info<< "Generating mesh for region " << regionName << endl;
        regionName  = args.option("region");
        regionPath = regionName;
    }

    // Locate appropriate blockMeshDict
#   include "findBlockMeshDict.H"

    blockMesh blocks(meshDict, regionName);


    if (args.optionFound("blockTopology"))
    {
        // Write mesh as edges.
        {
            fileName objMeshFile("blockTopology.obj");

            OFstream str(runTime.path()/objMeshFile);

            Info<< nl << "Dumping block structure as Lightwave obj format"
                << " to " << objMeshFile << endl;

            blocks.writeTopology(str);
        }

        // Write centres of blocks
        {
            fileName objCcFile("blockCentres.obj");

            OFstream str(runTime.path()/objCcFile);

            Info<< nl << "Dumping block centres as Lightwave obj format"
                << " to " << objCcFile << endl;

            const polyMesh& topo = blocks.topology();

            const pointField& cellCentres = topo.cellCentres();

            forAll(cellCentres, cellI)
            {
                //point cc = b.blockShape().centre(b.points());
                const point& cc = cellCentres[cellI];

                str << "v " << cc.x() << ' ' << cc.y() << ' ' << cc.z() << nl;
            }
        }

        Info<< nl << "end" << endl;

        return 0;
    }


    Info<< nl << "Creating polyMesh from blockMesh" << endl;

    word defaultFacesName = "defaultFaces";
    word defaultFacesType = emptyPolyPatch::typeName;
    polyMesh mesh
    (
        IOobject
        (
            regionName,
            runTime.constant(),
            runTime
        ),
        xferCopy(blocks.points()),           // could we re-use space?
        blocks.cells(),
        blocks.patches(),
        blocks.patchNames(),
        blocks.patchDicts(),
        defaultFacesName,
        defaultFacesType
    );


    // Read in a list of dictionaries for the merge patch pairs
    if (meshDict.found("mergePatchPairs"))
    {
        List<Pair<word> > mergePatchPairs
        (
            meshDict.lookup("mergePatchPairs")
        );

#       include "mergePatchPairs.H"
    }
    else
    {
        Info<< nl << "There are no merge patch pairs edges" << endl;
    }


    // Set any cellZones (note: cell labelling unaffected by above
    // mergePatchPairs)

    label nZones = blocks.numZonedBlocks();

    if (nZones > 0)
    {
        Info<< nl << "Adding cell zones" << endl;

        // Map from zoneName to cellZone index
        HashTable<label> zoneMap(nZones);

        // Cells per zone.
        List<dynamicLabelList > zoneCells(nZones);

        // Running cell counter
        label cellI = 0;

        // Largest zone so far
        label freeZoneI = 0;

        forAll(blocks, blockI)
        {
            const block& b = blocks[blockI];
            const labelListList& blockCells = b.cells();
            const word& zoneName = b.blockDef().zoneName();

            if (zoneName.size())
            {
                HashTable<label>::const_iterator iter = zoneMap.find(zoneName);

                label zoneI;

                if (iter == zoneMap.end())
                {
                    zoneI = freeZoneI++;

                    Info<< "    " << zoneI << '\t' << zoneName << endl;

                    zoneMap.insert(zoneName, zoneI);
                }
                else
                {
                    zoneI = iter();
                }

                forAll(blockCells, i)
                {
                    zoneCells[zoneI].append(cellI++);
                }
            }
            else
            {
                cellI += b.cells().size();
            }
        }


        List<cellZone*> cz(zoneMap.size());

        Info<< nl << "Writing cell zones as cellSets" << endl;

        forAllConstIter(HashTable<label>, zoneMap, iter)
        {
            label zoneI = iter();

            cz[zoneI] = new cellZone
            (
                iter.key(),
                zoneCells[zoneI].shrink(),
                zoneI,
                mesh.cellZones()
            );

            // Write as cellSet for ease of processing
            cellSet cset
            (
                mesh,
                iter.key(),
                labelHashSet(zoneCells[zoneI].shrink())
            );
            cset.write();
        }

        mesh.pointZones().setSize(0);
        mesh.faceZones().setSize(0);
        mesh.cellZones().setSize(0);
        mesh.addZones(List<pointZone*>(0), List<faceZone*>(0), cz);
    }

    // Set the precision of the points data to 10
    IOstream::defaultPrecision(max(10u, IOstream::defaultPrecision()));

    Info<< nl << "Writing polyMesh" << endl;
    mesh.removeFiles();
    if (!mesh.write())
    {
        FatalErrorInFunction
            << "Failed writing polyMesh."
            << exit(FatalError);
    }

    // Write summary
    {
        const polyPatchList& patches = mesh.boundaryMesh();

        Info<< "----------------" << nl
            << "Mesh Information" << nl
            << "----------------" << nl
            << "  " << "boundingBox: " << boundBox(mesh.points()) << nl
            << "  " << "nPoints: " << mesh.nPoints() << nl
            << "  " << "nCells: " << mesh.nCells() << nl
            << "  " << "nFaces: " << mesh.nFaces() << nl
            << "  " << "nInternalFaces: " << mesh.nInternalFaces() << nl;

        Info<< "----------------" << nl
            << "Patches" << nl
            << "----------------" << nl;

        forAll (patches, patchI)
        {
            const polyPatch& p = patches[patchI];

            Info<< "  " << "patch " << patchI
                << " (start: " << p.start()
                << " size: " << p.size()
                << ") name: " << p.name()
                << nl;
        }
    }

    Info<< "\nEnd\n" << endl;
}

