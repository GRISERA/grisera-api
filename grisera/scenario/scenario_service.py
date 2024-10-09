from typing import Union

from grisera.activity_execution.activity_execution_model import ActivityExecutionIn
from grisera.scenario.scenario_model import ScenarioIn, OrderChangeIn


class ScenarioService:
    """
    Abstract class to handle logic of scenarios requests

    """

    def save_scenario(self, scenario: ScenarioIn, dataset_id: Union[int, str]):
        """
        Send request to grisera api to create new scenario

        Args:
            scenario (ScenarioIn): Scenario to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as scenario object
        """
        raise Exception("save_scenario not implemented yet")

    def add_scenario_execution(self, scenario_id: Union[int, str], scenario: ScenarioIn, dataset_id: Union[int, str]):
        """
        Send request to grisera api to add scenario_execution to scenario

        Args:
            scenario_id (int | str): id of scenario to add scenario_execution to
            scenario (ScenarioIn): Scenario to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as activity_execution object
        """
        raise Exception("add_activity_execution not implemented yet")

    def update_scenario(self, scenario_id: Union[int, str], scenario: ScenarioIn, dataset_id: Union[int, str]):
        """
        Send request to grisera api to create new scenario

        Args:
            scenario_id (int | str): id of scenario to add scenario_execution to
            scenario (ScenarioIn): Scenario to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as scenario object
        """
        raise Exception("save_scenario not implemented yet")

    def add_activity_execution(self, previous_id: Union[int, str], activity_execution: ActivityExecutionIn,
                               dataset_id: Union[int, str]):
        """
        Send request to graph api to add activity_execution to scenario

        Args:
            previous_id (int | str): identity of previous activity_execution or experiment
            activity_execution (ActivityExecutionIn): ActivityExecution to be added
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as activity_execution object
        """
        raise Exception("add_activity_execution not implemented yet")

    def change_order_middle_with_last(self, middle_id: Union[int, str], last_id: Union[int, str],
                                      middle_relationships, last_relationships, dataset_id: Union[int, str]):
        """
            Changes order of the middle node and the last node

            Args:
                middle_id (int | str): identity of the middle node
                last_id (int | str): identity of the last node
                middle_relationships: Relationships of the middle node
                last_relationships: Relationships of the last node
                dataset_id (int | str): name of dataset
            Returns:
        """
        raise Exception("change_order_middle_with_last not implemented yet")

    def change_order_middle_with_middle(self, middle_id: Union[int, str], last_id: Union[int, str],
                                        middle_relationships, last_relationships, dataset_id: Union[int, str]):
        """
            Changes order of the two middle nodes

            Args:
                middle_id (int| str): identity of the middle node
                last_id (int | str): identity of the middle node but second in order
                middle_relationships: Relationships of the middle node
                last_relationships: Relationships of the last node
                dataset_id (int | str): name of dataset
            Returns:
        """
        raise Exception("change_order_middle_with_middle not implemented yet")

    def what_order(self, previous_relationships, activity_execution_relationships, dataset_id: Union[int, str]):
        """
            Finds which node is in which order (starting from experiment) in the scenario

            Args:
                previous_relationships: Relationships of the previous node
                activity_execution_relationships: Relationships of the activity execution node
                dataset_id (int | str): name of dataset
            Returns:
                True when is the first in order
                False when is the second in order
        """
        raise Exception("what_order not implemented yet")

    def swap_order_in_relationships_array(self, relationships, element_id: Union[int, str],
                                          dataset_id: Union[int, str]):
        """
            Swaps order of relationships list, so they are saved in order starting from experiment
            Args:
                relationships: List of relationships
                element_id: identity of element, that relationships belong to
                dataset_id (int | str): name of dataset
            Returns:
                relationships: List of relationships in specified order
        """
        raise Exception("swap_order_in_relationships_array not implemented yet")

    def change_order(self, order_change: OrderChangeIn, dataset_id: Union[int, str]):
        """
        Send request to graph api to change order in scenario

        Args:
            order_change (OrderChangeIn): Ids of activity_executions to change order by
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as changed order ids
        """
        raise Exception("change_order not implemented yet")

    def delete_activity_execution(self, activity_execution_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to graph api to delete activity_execution from scenario

        Args:
            activity_execution_id (int | str): identity of activity_execution to delete
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as activity_execution object
        """
        raise Exception("delete_activity_execution not implemented yet")

    def delete_scenario_execution(self, scenario_execution_id: Union[int, str], dataset_id: Union[int, str]):
        """
        Send request to graph api to delete scenario_execution from scenario

        Args:
            scenario_execution_id (int | str): identity of activity_execution to delete
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as scenario object
        """
        raise Exception("delete_activity_execution not implemented yet")

    def get_scenario(self, element_id: Union[int, str], dataset_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get activity executions and experiment from scenario

        Args:
            element_id (int | str): identity of experiment or activity execution which is included in scenario
            depth: (int): specifies how many related entities will be traversed to create the response
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as Scenario object
        """
        raise Exception("get_scenario not implemented yet")

    def get_scenario_by_experiment(self, experiment_id: Union[int, str], dataset_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get activity_executions from scenario which starts in experiment

        Args:
            experiment_id (int | str): identity of experiment where scenario starts
            depth: (int): specifies how many related entities will be traversed to create the response
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as Scenario object
        """
        raise Exception("get_scenario_by_experiment not implemented yet")

    def get_scenarios_by_experiment(self, experiment_id: Union[int, str], dataset_id: Union[int, str], depth: int = 0):
        """
        Send request to graph api to get activity_executions from scenario which starts in experiment

        Args:
            experiment_id (int | str): identity of experiment where scenario starts
            depth: (int): specifies how many related entities will be traversed to create the response
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as Scenario object
        """
        raise Exception("get_scenario_by_experiment not implemented yet")

    def get_scenario_by_activity_execution(self, activity_execution_id: Union[int, str], dataset_id: Union[int, str],
                                           depth: int = 0):
        """
        Send request to graph api to get activity_executions from scenario which has activity execution id included

        Args:
            activity_execution_id (int | str): identity of activity execution included in scenario
            depth: (int): specifies how many related entities will be traversed to create the response
            dataset_id (int | str): name of dataset

        Returns:
            Result of request as Scenario object
        """
        raise Exception("get_scenario_by_activity_execution not implemented yet")

    def get_scenario_after_activity_execution(self, activity_execution_id: Union[int, str], activity_executions: [],
                                              dataset_id: Union[int, str], depth: int = 0):
        """
        Gets activity executions from scenario which are saved after activity_execution_id

        Args:
            activity_execution_id (int | str): identity of activity execution included in scenario
            activity_executions: List of activity executions in scenario
            depth: (int): specifies how many related entities will be traversed to create the response
            dataset_id (int | str): name of dataset
        """
        raise Exception("get_scenario_after_activity_execution not implemented yet")

    def get_scenario_before_activity_execution(self, activity_execution_id: Union[int, str], activity_executions: [],
                                               dataset_id: Union[int, str], depth: int = 0):
        """
        Gets activity executions from scenario which are saved before activity_execution_id

        Args:
            activity_execution_id (int | str): identity of activity execution included in scenario
            activity_executions: List of activity executions in scenario
            depth: (int): specifies how many related entities will be traversed to create the response
            dataset_id (int | str): name of dataset
        """
        raise Exception("get_scenario_before_activity_execution not implemented yet")
