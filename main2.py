def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        file1_lines = f1.readlines()
        file2_lines = f2.readlines()

    differences = []
    
    # Verifica linha por linha
    for i, (line1, line2) in enumerate(zip(file1_lines, file2_lines)):
        if line1 != line2:
            differences.append(f"Linha {i+1} diferente:\n{file1}: {line1.strip()}\n{file2}: {line2.strip()}")
    
    # Caso um arquivo tenha mais linhas que o outro
    if len(file1_lines) > len(file2_lines):
        for i in range(len(file2_lines), len(file1_lines)):
            differences.append(f"Linha {i+1} diferente no {file1}: {file1_lines[i].strip()}")
    elif len(file2_lines) > len(file1_lines):
        for i in range(len(file1_lines), len(file2_lines)):
            differences.append(f"Linha {i+1} diferente no {file2}: {file2_lines[i].strip()}")
    
    return differences

# Exemplo de uso
file1 = 'CSO-7F_NEAR.xyz'
file2 = 'CSO-7F_FAR.xyz'

diff = compare_files(file1, file2)

# Exibir as diferenças
if diff:
    for d in diff:
        print(d)
else:
    print("Os arquivos são idênticos.")