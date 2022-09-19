from src.AF.AF import AF
from src.AF.Estado import Estado


def uniao_automatos(af1: AF, af2: AF) -> AF:
    # por conveniência na hora de apresentar resultados e debuggar,
    # vamos trocar os nomes dos estados do segundo AF
    af2.change_estados_nomes()

    af_new: AF = AF()
    af_new.qtd_estados = af1.qtd_estados + af2.qtd_estados + 1
    af_new.estados = af1.estados + af2.estados
    af_new.estados_finais = af1.estados_finais + af2.estados_finais

    for letra in af1.alfabeto + af2.alfabeto:
        if letra not in af_new.alfabeto:
            af_new.alfabeto.append(letra)

    af_new.is_deterministico = False

    # para fazer a união entre dois estados, é necessário
    # fazer um novo estado e fazer união por epsilon-transição
    # para seus antigos estados iniciais
    estado_new: Estado = Estado("EstadoUniao", af_new)
    estado_new.add_transicao("&", af1.estado_inicial)
    estado_new.add_transicao("&", af2.estado_inicial)
    af_new.estado_inicial = estado_new
    af_new.estado_now = af_new.estado_inicial

    return af_new