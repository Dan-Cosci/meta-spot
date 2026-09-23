import time
import pytest
from fastapi.testclient import TestClient

from main import app, PROCESS_QUE  # import the actual queue object


@pytest.fixture
def client():
    return TestClient(app)


def fill_queue_to_capacity(q):
    """Push dummy items directly onto the queue until it's full,
    bypassing the API so we don't need real workers or real jobs."""
    while not q.full():
        q.put_nowait(object())  # placeholder — the queue doesn't care what's in it for this test


def test_job_rejected_when_queue_full(client):
    fill_queue_to_capacity(PROCESS_QUE)
    assert PROCESS_QUE.full()

    start = time.monotonic()
    response = client.post("/job", json={"song": "test song"})
    elapsed = time.monotonic() - start

    assert response.status_code == 503
    assert response.json()["success"] is False
    # confirms it didn't hang forever, and roughly matches your retry deadline
    assert elapsed < 6  # adjust to your actual deadline + a small buffer
    assert elapsed > 1.5  # confirms it actually retried, not just failed instantly


def test_job_accepted_once_space_frees_up(client):
    fill_queue_to_capacity(PROCESS_QUE)

    # simulate a worker draining one job partway through the retry window
    import threading
    def free_a_slot():
        time.sleep(1)
        PROCESS_QUE.get_nowait()
    threading.Thread(target=free_a_slot).start()

    response = client.post("/job", json={"song": "test song"})
    assert response.status_code == 201
