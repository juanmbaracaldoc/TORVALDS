import subprocess


def ejecutar(comando):
    return subprocess.check_output(
        comando,
        shell=True,
        text=True
    ).strip()


def cifrado_cesar(caracter, desplazamiento):
    if not caracter.isalpha():
        return caracter

    base = ord('A') if caracter.isupper() else ord('a')

    return chr(
        (ord(caracter) - base + desplazamiento) % 26 + base
    )


llave = ""

commits = ejecutar(
    "git rev-list --reverse HEAD"
).splitlines()

for commit in commits:

    hash_completo = commit

    contenido = ejecutar(
        f"git show {commit}:nucleo.txt"
    )
    
    contenido = "".join(
        c for c in contenido
        if c.isprintable() and c not in "\r\n\t"
    )

    valor_decimal = int(
        hash_completo[:6],
        16
    )

    if valor_decimal % 2 == 0:

        primer_caracter = contenido[0]

        cantidad_numeros = sum(
            c.isdigit()
            for c in hash_completo
        )

        resultado = cifrado_cesar(
            primer_caracter,
            cantidad_numeros
        )

    else:

        ultimo_caracter = contenido[-1]

        cantidad_letras = sum(
            c in "abcdef"
            for c in hash_completo.lower()
        )

        resultado = chr(
            ord(ultimo_caracter) +
            cantidad_letras
        )

    llave += resultado

    padres = ejecutar(
        f"git rev-list --parents -n 1 {commit}"
    ).split()

    if len(padres) > 2:
        llave = llave[::-1]

print(repr(llave))