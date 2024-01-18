#include "patchAverage.H"
#include "fvCFD.H"

pyBindPatchAverage::pyBindPatchAverage(const word& fieldName, const word& patchName)
    : fieldName_(fieldName), patchName_(patchName) {}

pyBindPatchAverage::~pyBindPatchAverage() {
	Info << "pyBindPatchAverage destructor" << endl;
}

void pyBindPatchAverage::calculateAverages() {
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
#include "createTime.H"
	instantList timeDirs = timeSelector::select0(runTime, args);

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

