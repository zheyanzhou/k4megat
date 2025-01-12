#include "SimSaveTrajectory.h"
#include "SimKernel/Units.h"

// Geant4
#include "G4Event.hh"
#include "G4Trajectory.hh"
#include "G4VTrajectory.hh"

// datamodel
#include "edm4hep/TrackerHitCollection.h"

namespace megat {

  DECLARE_COMPONENT_WITH_ID( SimSaveTrajectory, "SimSaveTrajectory" )

  SimSaveTrajectory::SimSaveTrajectory( const std::string& aType, const std::string& aName, const IInterface* aParent )
      : GaudiTool( aType, aName, aParent ) {
    declareInterface<ISimSaveOutputTool>( this );
    declareProperty( "TrajectoryPoints", m_trackHits, "Handle for trajectory hits" );
  }

  SimSaveTrajectory::~SimSaveTrajectory() {}

  StatusCode SimSaveTrajectory::initialize() {
    if ( GaudiTool::initialize().isFailure() ) { return StatusCode::FAILURE; }
    return StatusCode::SUCCESS;
  }

  StatusCode SimSaveTrajectory::finalize() { return GaudiTool::finalize(); }

  StatusCode SimSaveTrajectory::saveOutput( const G4Event& aEvent ) {
    auto                   edmPositions        = m_trackHits.createAndPut();
    G4TrajectoryContainer* trajectoryContainer = aEvent.GetTrajectoryContainer();
    for ( size_t trajectoryIndex = 0; trajectoryIndex < trajectoryContainer->size(); ++trajectoryIndex ) {
      G4VTrajectory* theTrajectory = ( *trajectoryContainer )[trajectoryIndex];
      for ( int pointIndex = 0; pointIndex < theTrajectory->GetPointEntries(); ++pointIndex ) {
        auto trajectoryPoint = theTrajectory->GetPoint( pointIndex )->GetPosition();
        auto edmHit          = edmPositions->create();
        edmHit.setCellID( 0 );
        edmHit.setEDep( 0 );
        edmHit.setTime( 0 );
        edmHit.setPosition( {
            trajectoryPoint.x() * g42edm::length,
            trajectoryPoint.y() * g42edm::length,
            trajectoryPoint.z() * g42edm::length,
        } );
      }
    }

    return StatusCode::SUCCESS;
  }
} // namespace megat
