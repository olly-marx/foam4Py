#include "patchAverage.H"
#include "../utils/importObject.H"
#include "pyBindFOAM/fvCFDWrapper/fvCFDWrapper.H"
#include <string>
#include <vector>

patchAverage::patchAverage(const std::string fieldName, const std::string patchName, 
        const fvCFDWrapper& foamCase) : foamCase_(foamCase)
{
    fieldName_ = Foam::word(fieldName);
    patchName_ = Foam::word(patchName);
}

patchAverage::~patchAverage() {
	Info << "patchAverage destructor" << endl;
}

void patchAverage::calculateAverage() {
	timeSelector::addOptions();
	argList::validArgs.append("fieldName");
	argList::validArgs.append("patchName");

	std::vector<std::string> arguments = {"null", fieldName_, patchName_};

	std::vector<char*> argv_;
	for (const auto& arg : arguments)
		argv_.push_back((char*)arg.data());
	argv_.push_back(nullptr);

	int argc = argv_.size() - 1;
	char** argv = argv_.data();

#include "setRootCase.H"

	// # include "createTime.H" refactor
	Foam::Info<< "Create time\n" << Foam::endl;                                      

    const Foam::fileName rootPath = ".";
    const Foam::fileName caseName = ".";

    
											 
	Foam::Time runTime(foamCase_.getControlDict(), Foam::fileName("."), Foam::fileName("."), 
        Foam::word("system"), Foam::word("constant"), false);

	instantList timeDirs = timeSelector::select0(runTime, args);

	// # include "createMesh.H" refactor
	//Foam::Info                                                                   
	//    << "Create mesh for time = "                                             
	//    << runTime.timeName() << Foam::nl << Foam::endl;                         
	//									     
	//Foam::fvMesh mesh                                                            
	//(                                                                            
	//    Foam::IOobject                                                           
	//    (                                                                        
	//	Foam::fvMesh::defaultRegion,                                         
	//	runTime.timeName(),                                                  
	//	runTime,                                                             
	//	Foam::IOobject::MUST_READ                                            
	//    )                                                                        
	//);
#include "createMesh.H"

	forAll(timeDirs, timeI) {
	    runTime.setTime(timeDirs[timeI], timeI);
	    Info << "Time = " << runTime.timeName() << endl;

	    IOobject fieldHeader(
		fieldName_,
		runTime.timeName(),
		mesh,
		IOobject::MUST_READ
	    );

	    // Check field exists
	    if (fieldHeader.headerOk()) {
		mesh.readUpdate();

		label patchi = mesh.boundaryMesh().findPatchID(patchName_);
		if (patchi < 0) {
		    FatalError << "Unable to find patch " << patchName_ << endl
			       << exit(FatalError);
		}

		if (fieldHeader.headerClassName() == "volScalarField") {
		    Info << "    Reading volScalarField " << fieldName_ << endl;
		    volScalarField field(fieldHeader, mesh);

		    scalar area = gSum(mesh.magSf().boundaryField()[patchi]);
		    scalar sumField = 0;

		    if (area > 0) {
			sumField = gSum(
			    mesh.magSf().boundaryField()[patchi]
			  * field.boundaryField()[patchi]
			) / area;
		    }

		    Info << "    Average of " << fieldName_ << " over patch "
			 << patchName_ << '[' << patchi << ']' << " = "
			 << sumField << endl;
		} else {
		    FatalError << "Only possible to average volScalarFields " << endl
			       << exit(FatalError);
		}
	    } else {
		Info << "    No field " << fieldName_ << endl;
	    }

	    Info << endl;
	}

	Info << "End" << endl;
}

//void bindPatchAverage(py::module &m) {
//    // Bind patchAverage class to python
//}
