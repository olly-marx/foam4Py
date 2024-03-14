#include "pyPatchAverage.H"

pyPatchAverage::pyPatchAverage(const fvCFDWrapper& foamCase) : foamCase_(foamCase){}

pyPatchAverage::~pyPatchAverage() {
	Info << "patchAverage destructor" << endl;
}

void pyPatchAverage::runPatchAverage(pybind11::object pyargv11)
{
    arguments pyArgs = arguments(pyargv11);

	timeSelector::addOptions();
	argList::validArgs.append("fieldName");
	argList::validArgs.append("patchName");

    int argc = pyArgs.argc_;
    char **argv = pyArgs.argv_;

    // Print the command line arguments
    for (int i = 0; i < argc; i++) {
        Info << "argv[" << i << "] = " << argv[i] << endl;
    }

    word fieldName(argv[1]);
    word patchName(argv[2]);

#include "setRootCase.H"

	// # include "createTime.H" refactor
	Info<< "Create time\n" << endl;                                      

    const fileName rootPath = ".";
    const fileName caseName = ".";

    dictionary controlDict = utils::importDictionary(foamCase_, "system/controlDict");

    Info << "controlDict has been init to "<< controlDict << endl;

	Time runTime(controlDict, fileName("."), fileName("."), 
        word("system"), word("constant"), false);

	instantList timeDirs = timeSelector::select0(runTime, args);

#include "createMesh.H"

	forAll(timeDirs, timeI) {
	    runTime.setTime(timeDirs[timeI], timeI);
	    Info << "Time = " << runTime.timeName() << endl;

	    IOobject fieldHeader(
        fieldName,
		runTime.timeName(),
		mesh,
		IOobject::MUST_READ
	    );

	    // Check field exists
	    if (fieldHeader.headerOk()) {
		mesh.readUpdate();

		label patchi = mesh.boundaryMesh().findPatchID(patchName);
		if (patchi < 0) {
		    FatalError << "Unable to find patch " << patchName << endl
			       << exit(FatalError);
		}

		if (fieldHeader.headerClassName() == "volScalarField") {
		    Info << "    Reading volScalarField " << fieldName << endl;
		    volScalarField field(fieldHeader, mesh);

		    scalar area = gSum(mesh.magSf().boundaryField()[patchi]);
		    scalar sumField = 0;

		    if (area > 0) {
			sumField = gSum(
			    mesh.magSf().boundaryField()[patchi]
			  * field.boundaryField()[patchi]
			) / area;
		    }

		    Info << "    Average of " << fieldName << " on patch "
			 << patchName << '[' << patchi << ']' << " = "
			 << sumField << endl;
		} else {
		    FatalError << "Only possible to average volScalarFields " << endl
			       << exit(FatalError);
		}
	    } else {
		Info << "    No field " << fieldName << endl;
	    }

	    Info << endl;
	}

	Info << "End" << endl;
}

//void bindPatchAverage(py::module &m) {
//    // Bind patchAverage class to python
//}
