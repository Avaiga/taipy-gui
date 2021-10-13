from taipy.task.scheduler.executor.synchronous import Synchronous


def mult(nb1, nb2):
    return nb1 * nb2


def mult_by_two(nb):
    return mult(2, nb)


def test_submit_one_argument():
    res = Synchronous().submit(mult_by_two, 21)
    assert res.result() == 42


def test_submit_two_arguments():
    res = Synchronous().submit(mult, 21, 4)
    assert res.result() == 84


def test_submit_two_arguments_in_context_manager():
    with Synchronous() as pool:
        res = pool.submit(mult, 21, 4)
        assert res.result() == 84
