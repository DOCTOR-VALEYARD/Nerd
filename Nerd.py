#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PAINEL DENÚNCIAS • NERD LINUX
# Todos os direitos reservados © 2026
import os, sys, time, json, re, hashlib, random
from datetime import datetime, timedelta
import requests

# ==============================
# CORES — TOTALMENTE LILÁS
# ==============================
L1 = "\033[38;5;171m"
L2 = "\033[38;5;183m"
R = "\033[0m"

URL_API = "COLOQUE_SUA_URL_DA_API_AQUI"
BASE = "base_dados_nerd.json"
PENDENTES = "fila_envio.json"
TOTAL = 200000

OPERADORAS = ["Vivo", "Claro", "TIM", "Oi", "Algar", "Sercomtel"]
TECNOLOGIA = ["4G", "4G/5G", "5G", "3G/4G"]
TIPO_PLANO = ["Pré‑pago", "Pós‑pago", "Controle", "Empresarial"]

PAISES = {
    "+55": {"nome":"Brasil","sigla":"BR",
            "nomes":["Francisco Antônio","Maria Silva","João Pedro","Ana Clara","Carlos Alberto",
                     "Juliana Costa","Lucas Oliveira","Beatriz Santos","Pedro Henrique","Larissa Rodrigues",
                     "Marcos Vinícius","Camila Fernandes","Gustavo Lima","Letícia Almeida","Rafael Pereira"],
            "cidades":["São Paulo","Rio de Janeiro","Belo Horizonte","Salvador","Campinas","Ribeirão Preto"]},
    "+1": {"nome":"Estados Unidos","sigla":"US","nomes":["John Smith","Emma Johnson"],"cidades":["Nova York"]},
    "+351": {"nome":"Portugal","sigla":"PT","nomes":["João Pereira","Ana Martins"],"cidades":["Lisboa"]},
    "+54": {"nome":"Argentina","sigla":"AR","nomes":["Sofía López","Mateo García"],"cidades":["Buenos Aires"]},
    "+44": {"nome":"Reino Unido","sigla":"GB","nomes":["Oliver Taylor","Amelia Davies"],"cidades":["Londres"]},
    "+49": {"nome":"Alemanha","sigla":"DE","nomes":["Max Müller","Emma Schmidt"],"cidades":["Berlim"]},
    "+33": {"nome":"França","sigla":"FR","nomes":["Leroy Dubois","Manon Martin"],"cidades":["Paris"]},
    "+52": {"nome":"México","sigla":"MX","nomes":["Santiago Hernández","Regina García"],"cidades":["Cidade do México"]},
    "+57": {"nome":"Colômbia","sigla":"CO","nomes":["Valentina Ramírez","Samuel Gómez"],"cidades":["Bogotá"]},
    "+51": {"nome":"Peru","sigla":"PE","nomes":["Mía Flores","Dante Vargas"],"cidades":["Lima"]},
    "+34": {"nome":"Espanha","sigla":"ES","nomes":["Lucía Fernández","Alejandro Díaz"],"cidades":["Madri"]}
}

# ==============================
# BANNER E FORMATAÇÃO
# ==============================
def limpar(): os.system("clear")

def banner():
    limpar()
    print(f"""{L1}
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ███╗   ███╗██████╗  █████╗ ██████╗ ██╗   ██╗███████╗     ║
║   ████╗ ████║██╔══██╗██╔══██╗██╔══██╗██║   ██║██╔════╝     ║
║   ██╔████╔██║██████╔╝███████║██████╔╝██║   ██║█████╗       ║
║   ██║╚██╔╝██║██╔══██╗██╔══██║██╔══██╗██║   ██║██╔══╝       ║
║   ██║ ╚═╝ ██║██████╔╝██║  ██║██║  ██║╚██████╔╝███████╗     ║
║   ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝     ║
║                                                            ║
║          ✦  SISTEMA DENÚNCIAS • NERD LINUX  ✦              ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
{L2}           💻 Todos os direitos reservados © 2026{R}""")

def carregando():
    print(f"\n{L1}┅┄┅┄『 ✦ 』{R} Processando...")
    for _ in range(28):
        print(f"{L1}█{R}", end="", flush=True)
        time.sleep(0.035)
    print("\n")

def entrada():
    print(f"\n{L1}┅┄┅┄『 ✦ 』┄┅┄┅┄{R}")
    resp = input(f"{L2}NERD LINUX{L1}\n┅┄┅┄『 ✦ 』┄┅┄┅┄{R}\n➤ ")
    return resp

# ==============================
# TRATAMENTO NÚMERO
# ==============================
def padronizar(num):
    so_n = re.sub(r"[^0-9]","", num.strip())
    if not so_n: return ""
    if len(so_n) in (12,13) and so_n.startswith("55"):
        return f"+{so_n}"
    return f"+{so_n.lstrip('+')}"

def pegar_ddi(num):
    n = num.lstrip("+")
    for ddi in PAISES:
        if n.startswith(ddi.lstrip("+")):
            return ddi, PAISES[ddi]
    return "+??", {"nome":"País não identificado","sigla":"--",
                   "nomes":["Usuário"],"cidades":["Região"]}

def chave(num):
    return hashlib.sha256(num.encode()).hexdigest()[:20]

# ==============================
# DADOS FIXOS + PLANO
# ==============================
def dados_plano():
    inicio = datetime.now() - timedelta(days=random.randint(30, 1825))
    fim = inicio + timedelta(days=random.choice([30,90,180,365]))
    return {
        "operadora": random.choice(OPERADORAS),
        "tecnologia": random.choice(TECNOLOGIA),
        "tipo_plano": random.choice(TIPO_PLANO),
        "ativacao": inicio.strftime("%d/%m/%Y"),
        "vencimento": fim.strftime("%d/%m/%Y")
    }

def criar_base():
    if os.path.exists(BASE): return
    carregando()
    base = {}
    for _ in range(TOTAL):
        ddi = random.choice(list(PAISES))
        p = PAISES[ddi]
        if ddi == "+55":
            uf = random.choice([11,12,16,19,21,31,41,51,61,71,81])
            num = f"{ddi}{uf}{random.randint(900000000,999999999)}"
        else:
            num = f"{ddi}{random.randint(10000000,999999999)}"
        c = chave(num)
        base[c] = {
            "numero": num, "pais": p["nome"], "sigla": p["sigla"], "ddi": ddi,
            "nome": random.choice(p["nomes"]), "cidade": random.choice(p["cidades"]),
            "whatsapp": random.choice(["Sim","Não","Verificar"]),
            "banido": random.choice(["Não","Sim"]),
            "denuncias": random.randint(0,8),
            **dados_plano()
        }
    with open(BASE,"w",encoding="utf-8") as f:
        json.dump(base,f,ensure_ascii=False)

def buscar(num):
    criar_base()
    n = padronizar(num)
    if not n: return None
    c = chave(n)
    with open(BASE,"r",encoding="utf-8") as f:
        base = json.load(f)
    if c in base: return base[c]
    ddi, p = pegar_ddi(n)
    novo = {
        "numero":n,"pais":p["nome"],"sigla":p["sigla"],"ddi":ddi,
        "nome":random.choice(p["nomes"]),"cidade":random.choice(p["cidades"]),
        "whatsapp":"Verificar","banido":"Não","denuncias":0,**dados_plano()
    }
    base[c] = novo
    with open(BASE,"w",encoding="utf-8") as f:
        json.dump(base,f,ensure_ascii=False)
    return novo

# ==============================
# ENVIO TOTALMENTE SILENCIOSO
# ==============================
def guardar(dados):
    fila = json.load(open(PENDENTES)) if os.path.exists(PENDENTES) else []
    fila.append(dados)
    json.dump(fila, open(PENDENTES,"w"))

def enviar(dados):
    final = {**dados, "hora":time.ctime()}
    try:
        r = requests.post(URL_API,json=final,timeout=12,
                          headers={"Content-Type":"application/json"})
        if r.status_code in (200,201): return
    except: pass
    guardar(final)

# ==============================
# EXIBIÇÃO DOS DADOS
# ==============================
def mostrar(dados):
    print(f"\n{L1}• DADOS:{R}")
    linhas = [
        ("Número",dados["numero"]),("País",dados["pais"]),("DDI",dados["ddi"]),
        ("Nome",dados["nome"]),("Cidade",dados["cidade"]),
        ("Operadora",dados["operadora"]),("Rede",dados["tecnologia"]),
        ("Plano",dados["tipo_plano"]),("Ativado em",dados["ativacao"]),
        ("Válido até",dados["vencimento"]),("WhatsApp",dados["whatsapp"]),
        ("Situação",dados["banido"]),("Denúncias",dados["denuncias"])
    ]
    for t,v in linhas:
        print(f"{L1}┅┄『 ✦ 』{L2} {t}: {v}{R}")

# ==============================
# MENUS
# ==============================
def menu():
    while True:
        banner()
        print(f"""
{L1}┅┄┅┄『 ✦ 』{L2} 1 • Nova denúncia{L1}
┅┄┅┄『 ✦ 』{L2} 2 • Consultar{L1}
┅┄┅┄『 ✦ 』{L2} 3 • Sair{R}
""")
        op = entrada()
        if op == "1": denunciar()
        elif op == "2": consultar()
        elif op == "3": break
    print(f"\n{L1}Concluído{R}")

def denunciar():
    banner()
    d = buscar(entrada())
    if not d: return
    mostrar(d)
    print(f"\n{L1}• MOTIVO{L2}")
    print(f"{L1}┅┄『 ✦ 』{L2} 1 • Discriminação{L1}")
    print(f"{L1}┅┄『 ✦ 』{L2} 2 • Ofensa{L1}")
    print(f"{L1}┅┄『 ✦ 』{L2} 3 • Assédio{L1}")
    print(f"{L1}┅┄『 ✦ 』{L2} 4 • Outro{L1}")
    m = entrada()
    motivos = {"1":"Discriminação","2":"Ofensa","3":"Assédio"}
    final = {**d,"motivo":motivos.get(m,"Outro"),"detalhe":entrada()}
    carregando()
    enviar(final)
    input()

def consultar():
    banner()
    d = buscar(entrada())
    carregando()
    if d: mostrar(d)
    input()

if __name__ == "__main__":
    try: menu()
    except: print(f"{L1}{R}")

