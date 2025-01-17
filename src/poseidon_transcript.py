from starkware.cairo.common.poseidon_utils import PoseidonParams, hades_permutation
from src.hints.io import bigint_split
from src.definitions import N_LIMBS, BASE
from src.algebra import PyFelt, ModuloCircuitElement


class CairoPoseidonTranscript:
    """
    The CairoPoseidonTranscript class facilitates the emulation of Cairo's sequential hashing mechanism.
    Specifically, it sequentially computes hashes in the form of H = Poseidon(0, Poseidon(1, Poseidon(2, ...))).
    """

    def __init__(self, init_hash: int) -> None:
        self.params = PoseidonParams.get_default_poseidon_params()
        self.init_hash = init_hash
        self.s0, self.s1, self.s2 = hades_permutation([init_hash, 0, 1], self.params)
        self.permutations_count = 1
        self.poseidon_ptr_indexes = []
        self.z = None

    @property
    def continuable_hash(self) -> int:
        return self.s0

    @property
    def RLC_coeff(self):
        """
        A function to retrieve the random linear combination coefficient after a permutation.
        Stores the index of the last permutation in the poseidon_ptr_indexes list, to be used to retrieve RLC coefficients later.
        """
        self.poseidon_ptr_indexes.append(self.permutations_count - 1)
        return self.s1

    def hash_element(self, x: PyFelt | ModuloCircuitElement):
        # print(f"Will Hash PYTHON {hex(x.value)}")
        limbs = bigint_split(x.value, N_LIMBS, BASE)
        self.s0, self.s1, self.s2 = hades_permutation(
            [
                self.s0 + limbs[0] + (BASE) * limbs[1],
                self.s1 + limbs[2] + (BASE) * limbs[3],
                self.s2,
            ],
            self.params,
        )
        self.permutations_count += 1

        return self.s0, self.s1

    def hash_limbs_multi(
        self, X: list[PyFelt | ModuloCircuitElement], sparsity: list[int] = None
    ) -> tuple[int, int]:
        if sparsity:
            X = [x for i, x in enumerate(X) if sparsity[i] != 0]
        for X_elem in X:
            self.hash_element(X_elem)
        return self.s0, self.s1
