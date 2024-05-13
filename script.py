import re


def generate_python_code_from_feature(feature_text):
    step_patterns = {'Given': '@given', 'When': '@when', 'Then': '@then'}
    generated_code = []
    steps_set = set()
    previous_step = None

    for line in feature_text.split('\n'):
        line = line.strip()

        # Ignora linhas que não são do cenário ou estão em branco
        if not line or line.startswith(('Feature:', 'Scenario:')):
            continue

        # Processa apenas linhas dentro de cenários
        if line.startswith(('Given', 'When', 'Then', 'And')):
            step_match = re.match(r'(Given|When|Then|And)(.*)', line)
            if step_match:
                step_type, step_text = step_match.groups()
                step_type = step_type.strip()
                step_text = step_text.strip()

                # Se a etapa for "AND", associa-a à palavra-chave anterior
                if step_type == 'And':
                    if previous_step is None:
                        continue  # Ignora o "AND" no início do cenário
                    step_type = previous_step

                if step_text:
                    # Verifica se a palavra-chave da etapa é válida
                    if step_type in step_patterns:
                        step_key = f"{step_patterns[step_type]}('{step_text}')"
                        if step_key not in steps_set:
                            steps_set.add(step_key)
                            generated_code.append(f"{step_patterns[step_type]}('{step_text}')")
                            generated_code.append("def step_impl(context):")
                            generated_code.append("\traise NotImplementedError()\n")
                            # Atualiza a palavra-chave anterior
                            previous_step = step_type

    return '\n'.join(generated_code)


if __name__ == '__main__':
    with open('example.feature', 'r') as file:
        feature_text = file.read()

    generated_code = generate_python_code_from_feature(feature_text)

    with open('arquivo.py', 'w') as file:
        file.write(generated_code)
