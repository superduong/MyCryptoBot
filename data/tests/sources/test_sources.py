from data.service.external_requests import generate_signal
from data.service.helpers import MODEL_APP_ENDPOINTS
from data.sources._signal_triggerer import wait_for_job_conclusion
from data.sources import trigger_signal
from shared.utils.tests.fixtures.external_modules import mock_time_sleep
from data.tests.setup.fixtures.internal_modules import *
from data.tests.setup.fixtures.external_modules import *
from shared.utils.exceptions import FailedSignalGeneration

from pytest_mock import mocker
import pytest


class TestExternalRequests:

    @pytest.mark.parametrize(
        "side_effects,expected_value",
        [
            pytest.param(
                [
                    {"status": "finished"},
                ],
                True,
                id="STATUS_FINISHED",
            ),
            pytest.param(
                [
                    {"status": "in-queue"},
                    {"status": "waiting"},
                    {"status": "waiting"},
                    {"status": "finished"},
                ],
                True,
                id="STATUS_WAITING_IN-QUEUE",
            ),
            pytest.param(
                [
                    {"status": "failed"},
                ],
                False,
                id="STATUS_FAILED",
            ),
            pytest.param(
                [
                    {"status": "job not found"},
                    {"status": "finished"},
                ],
                True,
                id="STATUS_NOT_FOUND",
            ),
        ],
    )
    def test_wait_for_job_conclusion(
        self,
        side_effects,
        expected_value,
        mock_check_job_status_response,
        mock_generate_signal,
        mock_time_sleep,
        mock_redis_connection_1,
    ):
        """
        GIVEN some params
        WHEN the method generate_signal is called
        THEN the return value is equal to the expected response

        """

        mock_generate_signal.side_effect = [{"success": True, "job_id": 'abcdef'}] * len(side_effects)
        mock_check_job_status_response.side_effect = side_effects

        params = {
            "job_id": "abcdef",
            "pipeline_id": 1,
            "retry": 0
        }

        res = wait_for_job_conclusion(**params)

        assert res == expected_value

        assert mock_check_job_status_response.call_count == len(side_effects)

    def test_wait_for_job_conclusion_exception(
        self,
        mock_check_job_status_response,
        mock_generate_signal,
        mock_redis_connection_1,
        mock_time_sleep
    ):

        mock_generate_signal.return_value = {"success": True, "job_id": 'abcdef'}
        # mock_redis_connection.return_value = mocked_redis

        mock_check_job_status_response.side_effect = [
            {"status": "job not found"},
            {"status": "job not found"},
            {"status": "job not found"},
            {"status": "job not found"},
            {"status": "job not found"},
            {"status": "finished"},
        ]

        params = {
            "job_id": "abcdef",
            "pipeline_id": 1,
            "retry": 0
        }

        with pytest.raises(FailedSignalGeneration) as excinfo:
            res = wait_for_job_conclusion(**params)

        assert excinfo.type == FailedSignalGeneration

    @pytest.mark.parametrize(
        "return_value,expected_value",
        [
            pytest.param(
                {"success": True, "job_id": 'abcdef'},
                True,
                id="SUCCESS",
            ),
            pytest.param(
                {"success": False, "response": "Failed"},
                False,
                id="FAIL",
            )
        ],
    )
    def test_trigger_signal(
        self,
        return_value,
        expected_value,
        mock_generate_signal,
        mock_redis_connection_1,
        mock_wait_for_job_conclusion,
    ):
        """
        GIVEN some params
        WHEN the method generate_signal is called
        THEN the return value is equal to the expected response

        """

        mock_generate_signal.return_value = return_value
        mock_wait_for_job_conclusion.return_value = True
        # mock_redis_connection.return_value = mocked_redis

        params = {
            "pipeline_id": 1,
            "retry": 0
        }

        res = trigger_signal(**params)

        assert res is expected_value
