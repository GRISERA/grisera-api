from grisera.activity.activity_service import ActivityService
from grisera.activity_execution.activity_execution_service import ActivityExecutionService
from grisera.appearance.appearance_service import AppearanceService
from grisera.arrangement.arrangement_service import ArrangementService
from grisera.channel.channel_service import ChannelService
from grisera.dataset.dataset_service import DatasetService
from grisera.experiment.experiment_service import ExperimentService
from grisera.life_activity.life_activity_service import LifeActivityService
from grisera.measure.measure_service import MeasureService
from grisera.measure_name.measure_name_service import MeasureNameService
from grisera.modality.modality_service import ModalityService
from grisera.observable_information.observable_information_service import ObservableInformationService
from grisera.participant.participant_service import ParticipantService
from grisera.participant_state.participant_state_service import ParticipantStateService
from grisera.participation.participation_service import ParticipationService
from grisera.personality.personality_service import PersonalityService
from grisera.recording.recording_service import RecordingService
from grisera.registered_channel.registered_channel_service import RegisteredChannelService
from grisera.registered_data.registered_data_service import RegisteredDataService
from grisera.scenario.scenario_service import ScenarioService
from grisera.services.service_factory import ServiceFactory
from grisera.time_series.time_series_service import TimeSeriesService


class NotImplementedServiceFactory(ServiceFactory):
    def get_dataset_service(self) -> DatasetService:
        pass

    def get_activity_service(self) -> ActivityService:
        pass

    def get_activity_execution_service(self) -> ActivityExecutionService:
        pass

    def get_appearance_service(self) -> AppearanceService:
        pass

    def get_arrangement_service(self) -> ArrangementService:
        pass

    def get_channel_service(self) -> ChannelService:
        pass

    def get_experiment_service(self) -> ExperimentService:
        pass

    def get_life_activity_service(self) -> LifeActivityService:
        pass

    def get_measure_service(self) -> MeasureService:
        pass

    def get_measure_name_service(self) -> MeasureNameService:
        pass

    def get_modality_service(self) -> ModalityService:
        pass

    def get_observable_information_service(self) -> ObservableInformationService:
        pass

    def get_participant_service(self) -> ParticipantService:
        pass

    def get_participant_state_service(self) -> ParticipantStateService:
        pass

    def get_participation_service(self) -> ParticipationService:
        pass

    def get_personality_service(self) -> PersonalityService:
        pass

    def get_recording_service(self) -> RecordingService:
        pass

    def get_registered_channel_service(self) -> RegisteredChannelService:
        pass

    def get_registered_data_service(self) -> RegisteredDataService:
        pass

    def get_scenario_service(self) -> ScenarioService:
        pass

    def get_time_series_service(self) -> TimeSeriesService:
        pass
