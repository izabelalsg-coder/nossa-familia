"""
Gerador de planos de leitura biblica (anual e semestral).

Distribui os 1189 capitulos da Biblia (canone protestante, traducao ARC,
mesma usada no Nossa Familia) em ordem canonica ao longo de N dias,
de forma proporcional. Gera um JSON pronto para ser consumido pelo app.

Uso:
    python3 gerar_planos.py
Saida:
    planos_leitura.json
"""

import json
import math

# Ordem canonica dos livros e numero de capitulos de cada um.
LIVROS = [
    ("Genesis", 50), ("Exodo", 40), ("Levitico", 27), ("Numeros", 36),
    ("Deuteronomio", 34), ("Josue", 24), ("Juizes", 21), ("Rute", 4),
    ("1 Samuel", 31), ("2 Samuel", 24), ("1 Reis", 22), ("2 Reis", 25),
    ("1 Cronicas", 29), ("2 Cronicas", 36), ("Esdras", 10), ("Neemias", 13),
    ("Ester", 10), ("Jo", 42), ("Salmos", 150), ("Proverbios", 31),
    ("Eclesiastes", 12), ("Cantares", 8), ("Isaias", 66), ("Jeremias", 52),
    ("Lamentacoes", 5), ("Ezequiel", 48), ("Daniel", 12), ("Oseias", 14),
    ("Joel", 3), ("Amos", 9), ("Obadias", 1), ("Jonas", 4), ("Miqueias", 7),
    ("Naum", 3), ("Habacuque", 3), ("Sofonias", 3), ("Ageu", 2),
    ("Zacarias", 14), ("Malaquias", 4),
    ("Mateus", 28), ("Marcos", 16), ("Lucas", 24), ("Joao", 21),
    ("Atos", 28), ("Romanos", 16), ("1 Corintios", 16), ("2 Corintios", 13),
    ("Galatas", 6), ("Efesios", 6), ("Filipenses", 4), ("Colossenses", 4),
    ("1 Tessalonicenses", 5), ("2 Tessalonicenses", 3), ("1 Timoteo", 6),
    ("2 Timoteo", 4), ("Tito", 3), ("Filemom", 1), ("Hebreus", 13),
    ("Tiago", 5), ("1 Pedro", 5), ("2 Pedro", 3), ("1 Joao", 5),
    ("2 Joao", 1), ("3 Joao", 1), ("Judas", 1), ("Apocalipse", 22),
]

TOTAL_CAPITULOS = sum(c for _, c in LIVROS)  # 1189


def flatten_capitulos():
    """Retorna lista de tuplas (livro, capitulo) em ordem canonica."""
    lista = []
    for livro, n_cap in LIVROS:
        for cap in range(1, n_cap + 1):
            lista.append((livro, cap))
    return lista


def formatar_dia(itens):
    """
    Recebe uma lista de (livro, capitulo) referentes a um mesmo dia
    e formata como texto legivel, agrupando capitulos consecutivos
    do mesmo livro em intervalos (ex: 'Genesis 1-3').
    Se o dia cruzar mais de um livro, os grupos sao separados por ';'.
    """
    grupos = []
    livro_atual = None
    inicio = None
    fim = None

    for livro, cap in itens:
        if livro == livro_atual and cap == fim + 1:
            fim = cap
        else:
            if livro_atual is not None:
                grupos.append((livro_atual, inicio, fim))
            livro_atual = livro
            inicio = cap
            fim = cap
    if livro_atual is not None:
        grupos.append((livro_atual, inicio, fim))

    partes = []
    for livro, ini, fim in grupos:
        if ini == fim:
            partes.append(f"{livro} {ini}")
        else:
            partes.append(f"{livro} {ini}-{fim}")
    return "; ".join(partes)


def gerar_plano(n_dias, nome_plano):
    capitulos = flatten_capitulos()
    total = len(capitulos)
    base = total // n_dias
    resto = total % n_dias

    dias = []
    idx = 0
    for dia in range(1, n_dias + 1):
        qtd = base + (1 if dia <= resto else 0)
        itens = capitulos[idx: idx + qtd]
        idx += qtd
        if not itens:
            continue
        dias.append({
            "dia": dia,
            "referencia": formatar_dia(itens),
            "livro_inicial": itens[0][0],
            "capitulo_inicial": itens[0][1],
            "livro_final": itens[-1][0],
            "capitulo_final": itens[-1][1],
            "total_capitulos_dia": qtd,
        })

    return {
        "id": nome_plano,
        "nome": "Plano Anual" if n_dias >= 300 else "Plano Semestral",
        "duracao_dias": n_dias,
        "total_capitulos": total,
        "dias": dias,
    }


def main():
    plano_anual = gerar_plano(365, "plano_anual")
    plano_semestral = gerar_plano(180, "plano_semestral")

    saida = {
        "planos": [plano_anual, plano_semestral],
        "meta": {
            "total_capitulos_biblia": TOTAL_CAPITULOS,
            "traducao": "ARC",
            "gerado_por": "gerar_planos.py",
        },
    }

    with open("planos_leitura.json", "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=2)

    print(f"Total de capitulos: {TOTAL_CAPITULOS}")
    print(f"Plano anual: {len(plano_anual['dias'])} dias")
    print(f"Plano semestral: {len(plano_semestral['dias'])} dias")
    print("Arquivo gerado: planos_leitura.json")


if __name__ == "__main__":
    main()
