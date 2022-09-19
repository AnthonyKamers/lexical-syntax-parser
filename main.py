from src.AF.AF import AF
from src.utils.UtilsAF import uniao_automatos

if __name__ == '__main__':
    af1: AF = AF()
    af1.parse_file("entradas/AF/exemplo1.af")
    af2: AF = AF()
    af2.parse_file("entradas/AF/exemplo1.af")

    af_new: AF = uniao_automatos(af1, af2)
    print(af_new)