# test para probar pytest de manera simple

def sumar(a, b):
    return a + b

def test_suma_basica():
    """Test simple: 2 + 2 debe ser 4."""
    resultado = sumar(2, 2)
    assert resultado == 4

def test_suma_con_negativos():
    """Test con números negativos: -3 + 1 debe ser -2."""
    resultado = sumar(-3, 1)
    assert resultado == -2