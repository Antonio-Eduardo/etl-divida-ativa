DATA_INSCRICAO — str -> precisa virar datetime

INDICADOR_AJUIZADO — str (SIM/NAO) -> pode virar booleano True/False

NUMERO_INSCRICAO — float64 -> deveria ser str, pois é um código identificador, não um número para calcular

Colunas de texto — aplicar .strip() para remover espaços em branco nas bordas