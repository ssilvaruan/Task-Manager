#!/usr/bin/env python3
"""TaskCLI - gerenciador de tarefas simples para o terminal."""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

# O arquivo fica na mesma pasta do script, não importa de onde ele é executado.
ARQUIVO = Path(__file__).resolve().parent / "tarefas.json"


def carregar():
    """Lê as tarefas do JSON. Retorna lista vazia se o arquivo não existir."""
    if not ARQUIVO.exists():
        return []
    try:
        with ARQUIVO.open(encoding="utf-8") as f:
            dados = json.load(f)
    except json.JSONDecodeError:
        sys.exit(f"Erro: {ARQUIVO.name} está corrompido. Corrija ou apague o arquivo.")
    if not isinstance(dados, list):
        sys.exit(f"Erro: {ARQUIVO.name} deve conter uma lista de tarefas.")
    return dados


def salvar(tarefas):
    """Grava de forma atômica para não corromper o arquivo se algo falhar."""
    fd, tmp = tempfile.mkstemp(dir=ARQUIVO.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(tarefas, f, ensure_ascii=False, indent=2)
        os.replace(tmp, ARQUIVO)
    except BaseException:
        os.unlink(tmp)
        raise


def adicionar(args):
    titulo = args.titulo.strip()
    if not titulo:
        sys.exit("Erro: o título da tarefa não pode ser vazio.")
    tarefas = carregar()
    novo_id = max((t["id"] for t in tarefas), default=0) + 1
    tarefas.append({"id": novo_id, "titulo": titulo, "feita": False})
    salvar(tarefas)
    print(f"Tarefa #{novo_id} adicionada.")


def listar(args):
    tarefas = carregar()
    if args.pendentes:
        tarefas = [t for t in tarefas if not t["feita"]]
    if not tarefas:
        print("Nenhuma tarefa encontrada.")
        return
    for t in tarefas:
        marca = "[x]" if t["feita"] else "[ ]"
        print(f"{t['id']:>3} {marca} {t['titulo']}")


def concluir(args):
    tarefas = carregar()
    tarefa = next((t for t in tarefas if t["id"] == args.id), None)
    if tarefa is None:
        sys.exit(f"Tarefa #{args.id} não encontrada.")
    if tarefa["feita"]:
        print(f"Tarefa #{args.id} já estava concluída.")
        return
    tarefa["feita"] = True
    salvar(tarefas)
    print(f"Tarefa #{args.id} concluída.")


def remover(args):
    tarefas = carregar()
    restantes = [t for t in tarefas if t["id"] != args.id]
    if len(restantes) == len(tarefas):
        sys.exit(f"Tarefa #{args.id} não encontrada.")
    salvar(restantes)
    print(f"Tarefa #{args.id} removida.")


def criar_parser():
    parser = argparse.ArgumentParser(description="TaskCLI - gerenciador de tarefas")
    sub = parser.add_subparsers(required=True, metavar="comando")

    p = sub.add_parser("add", help="adiciona uma tarefa")
    p.add_argument("titulo")
    p.set_defaults(func=adicionar)

    p = sub.add_parser("list", help="lista as tarefas")
    p.add_argument("-p", "--pendentes", action="store_true",
                   help="mostra só as tarefas não concluídas")
    p.set_defaults(func=listar)

    p = sub.add_parser("done", help="conclui uma tarefa pelo ID")
    p.add_argument("id", type=int)
    p.set_defaults(func=concluir)

    p = sub.add_parser("remove", help="remove uma tarefa pelo ID")
    p.add_argument("id", type=int)
    p.set_defaults(func=remover)

    return parser


def main():
    args = criar_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
