%builtins range_check poseidon range_check96 add_mod mul_mod

from starkware.cairo.common.cairo_builtins import PoseidonBuiltin, ModBuiltin
from starkware.cairo.common.registers import get_fp_and_pc
from starkware.cairo.common.alloc import alloc

from src.modulo_circuit import (
    run_extension_field_modulo_circuit,
    run_extension_field_modulo_circuit_continuation,
)
from src.definitions import bn, bls, UInt384, N_LIMBS, BASE, E12D

from src.precompiled_circuits.extf_mul import get_FP12_MUL_circuit

from src.modulo_circuit import ExtensionFieldModuloCircuit

func main{
    range_check_ptr,
    poseidon_ptr: PoseidonBuiltin*,
    range_check96_ptr: felt*,
    add_mod_ptr: ModBuiltin*,
    mul_mod_ptr: ModBuiltin*,
}() {
    alloc_locals;
    let (__fp__, _) = get_fp_and_pc();
    let (local input_bn: felt*) = alloc();
    let (local input_bls: felt*) = alloc();

    local expected_bn: E12D;
    local expected_bls: E12D;

    %{
        from random import randint
        import random
        from src.definitions import CURVES, PyFelt
        from src.hints.io import bigint_split, flatten, pack_e12d, fill_e12d
        random.seed(0)

        def generate_input_for_fp_mul(ptr:object, curve_id: int, extension_degree:int) -> list:
            p = CURVES[curve_id].p
            X = [PyFelt(randint(0, p - 1), p) for _ in range(2*extension_degree)]
            X = flatten([bigint_split(x.value, ids.N_LIMBS, ids.BASE) for x in X])
            segments.write_arg(ptr, X)
            return X

        generate_input_for_fp_mul(ids.input_bn, ids.bn.CURVE_ID, 12)
        generate_input_for_fp_mul(ids.input_bls, ids.bls.CURVE_ID, 12)
        #fill_e12d(ids.expected_bn, 4, 2**96)
        #fill_e12d(ids.expected_bls, 4, 2**96)
    %}

    let (circuit) = get_FP12_MUL_circuit(bn.CURVE_ID);
    let (output, _) = run_extension_field_modulo_circuit(circuit, input_bn);
    local res_bn: E12D = [cast(output, E12D*)];

    // let (circuit) = get_FP12_MUL_circuit(bls.CURVE_ID);
    // let (output, _) = run_extension_field_modulo_circuit(circuit, input_bls);
    // local res_bls: E12D = [cast(output, E12D*)];
    // %{
    //     res_bn = pack_e12d(ids.res_bn, 4, 2**96)
    //     res_bls = pack_e12d(ids.res_bls, 4, 2**96)
    //     print(f"res_bn: {res_bn}")
    //     print(f"expected_bn: {expected_outputs[0]}")
    //     print(f"res_bls: {res_bls}")
    //     print(f"expected_bls: {expected_outputs[1]}")
    //     assert res_bn == expected_outputs[0]
    //     assert res_bls == expected_outputs[1]
    //     print(f"Test passed")
    // %}

    return ();
}
