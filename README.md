# Problema de corte unidimensional via padrões de corte
Este é o clássico Problema de Corte, um desafio de otimização combinatória amplamente utilizado na indústria para minimizar o desperdício de material. O objetivo principal é determinar a forma mais rentável de cortar grandes barras de matéria-prima (como bobinas, vigas de aço ou tubos de tamanho fixo) em peças mais pequenas com comprimentos específicos, garantindo que se satisfaz a procura exata exigida por um projeto ou cliente.

A modelagem desse problema divide-se em duas fases.

- **Primeiro:** O algoritmo gera uma matriz de padrões de corte, gerando todas as combinações possíveis de peças que cabem dentro da barra original
- **Segundo:** Aplica o modelo de programação linear inteira, para minimizar o número total de barras inteiras processadas.

# O Problema
Uma fábrica de papel trabalha com a produção de bobinas para impressoras. Bobinas grandes de comprimento L são cortadas em itens menores de comprimento l1, l2, . . . , ln de acordo com as demandas D1, D2, . . . , Dn de cada um dos n tipos de bobinas menores.

a) Determine qual a melhor maneira de cortar as bobinas grandes em estoque de modo a atender à demanda e que minimize o número de bobinas grandes utilizadas. Dica: determine todos os possíveis padrões de corte das bobinas grandes nos tamanhos menores requeridos e então modele de forma a escolher padrões que forneçam melhor resultado.

b) Utilizar uma grande número de padrões de corte para o atendimento da demanda pode ter custo elevado para a empresa (muitos ajustes devem ser feitos nas máquinas de corte). Modifique seu modelo de forma que seja permitido utilizar no máximo um número m de padrões de corte. Qual o resultado obtido?
