import subprocess

resultado = subprocess.run(
    ["ls", "-la"],
    capture_output=True,
    text=True
)

print(resultado.stdout)
