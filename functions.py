import numpy as np
import sys

np.set_printoptions(
    precision=3,
    threshold=sys.maxsize
)


def generate_states() -> list[int]:
    """
    :return: List of all 40 states.
    """
    return list(range(40))


def dt_proba(state_1: int, state_2: int) -> float:
    """
    :param state_1:
    :param state_2:
    :return: Probability to transition from ``state_1`` to ``state_2`` due to dice roll.
    """
    dice_probas = [1/36, 2/36, 3/36, 4/36, 5/36, 6/36, 5/36, 4/36, 3/36, 2/36, 1/36]
    num_spaces = (state_2 - state_1) % 40
    if 2 <= num_spaces <= 12:
        return dice_probas[num_spaces - 2]
    return 0


def ast_proba(state_1: int, state_2: int) -> float:
    """
    :param state_1:
    :param state_2:
    :return: Probability to transition from ``state_1`` to ``state_2`` due to action space.
    """
    if state_1 not in [7, 22, 37, 4, 17, 33, 30]:  # state_1 is not an action space
        return 1 if state_1 == state_2 else 0
    elif state_1 == 30:  # state_1 is the "Go To Jail" space
        return 1 if state_2 == 10 else 0
    elif state_1 in [4, 17, 33]:  # state_1 is a chance space
        if state_1 == state_2:
            return 15/16
        elif state_2 == 10:
            return 1/16
        return 0
    else:  # state_1 is a surprise space (community chest)
        if state_1 == state_2:
            return 11/16
        elif state_2 in [0, 23, 10, 6, state_1 - 5]:
            return 1/16
        return 0


def dt_matrix() -> list[list[float]]:
    """
    :return: Dice transition matrix.
    """
    states = generate_states()
    return [[dt_proba(i, j) for j in states] for i in states]


def ast_matrix() -> list[list[float]]:
    """
    :return: Action space transition matrix.
    """
    states = generate_states()
    return [[ast_proba(i, j) for j in states] for i in states]


def t_matrix() -> np.ndarray:
    """
    :return: One step transition matrix.
    """
    return np.matmul(dt_matrix(), ast_matrix())


def generate_init_vector() -> list[float]:
    """
    :return: Initial probability distribution vector.
    """
    return [1] + [0] * 39


def generate_stationary_vector() -> np.ndarray:
    """
    :return: Stationary probability distribution vector.
    """
    eigen_values, eigen_vectors = np.linalg.eig(t_matrix().T)
    unit_vector = eigen_vectors[:, np.isclose(eigen_values, 1)][:, 0]
    stationary = unit_vector / unit_vector.sum()
    return stationary.real
