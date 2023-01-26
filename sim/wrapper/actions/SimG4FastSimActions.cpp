#include "SimG4FastSimActions.h"

// FCCSW
#include "SimG4Common/FastSimActions.h"

DECLARE_COMPONENT(SimG4FastSimActions)

SimG4FastSimActions::SimG4FastSimActions(const std::string& type, const std::string& name, const IInterface* parent)
    : AlgTool(type, name, parent) {
  declareInterface<ISimG4ActionTool>(this);
}

SimG4FastSimActions::~SimG4FastSimActions() {}

StatusCode SimG4FastSimActions::initialize() {
  if (AlgTool::initialize().isFailure()) {
    return StatusCode::FAILURE;
  }
  return StatusCode::SUCCESS;
}

StatusCode SimG4FastSimActions::finalize() { return AlgTool::finalize(); }

G4VUserActionInitialization* SimG4FastSimActions::userActionInitialization() { return new sim::FastSimActions(); }
