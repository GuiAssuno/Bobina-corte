# Problema de corte unidimensional via padrões de corte
Este é o clássico Problema de Corte, um desafio de otimização combinatória amplamente utilizado na indústria para minimizar o desperdício de material. O objetivo principal é determinar a forma mais rentável de cortar grandes barras de matéria-prima (como bobinas, vigas de aço ou tubos de tamanho fixo) em peças mais pequenas com comprimentos específicos, garantindo que se satisfaz a procura exata exigida por um projeto ou cliente.

A modelagem desse problema divide-se em duas fases.

- **Primeiro:** O algoritmo gera uma matriz de padrões de corte, gerando todas as combinações possíveis de peças que cabem dentro da barra original
- **Segundo:** Aplica o modelo de programação linear inteira, para minimizar o número total de barras inteiras processadas.

<br>

# O Problema
Uma fábrica de papel trabalha com a produção de bobinas para impressoras. Bobinas grandes de comprimento L são cortadas em itens menores de comprimento l1, l2, . . . , ln de acordo com as demandas D1, D2, . . . , Dn de cada um dos n tipos de bobinas menores.

a) Determine qual a melhor maneira de cortar as bobinas grandes em estoque de modo a atender à demanda e que minimize o número de bobinas grandes utilizadas. Dica: determine todos os possíveis padrões de corte das bobinas grandes nos tamanhos menores requeridos e então modele de forma a escolher padrões que forneçam melhor resultado.

b) Utilizar uma grande número de padrões de corte para o atendimento da demanda pode ter custo elevado para a empresa (muitos ajustes devem ser feitos nas máquinas de corte). Modifique seu modelo de forma que seja permitido utilizar no máximo um número m de padrões de corte. Qual o resultado obtido?

<br>

# Modelo Matemático Algébrico
No modelo algébrico, definimos a estrutura matemática generalizada usando conjuntos e somatórios, sem amarrar aos números específicos do problema.

**Conjuntos:**
- $i$: Conjunto de comprimentos dos cortes das demandas, $i = 1, \dots, n$.
- $j$: Conjunto de padrões de corte possíveis, $j = 1, \dots, P\quad \text{(Maximo de padrões)}$.

**Parâmetros:**
- $D_i$: Demanda exigida para o corte do tipo $i$.
- $Q_{ji}$: Quantidade de cortes do tipo $i$ ao utilizar o padrão $j$.
- $m$: Número máximo de padrões de cortes que podem ser utilizados.
- $M$: Um número arbitrariamente grande (Big-M, equivalente a $\sum D_i$).


**Variáveis de Decisão:**
- $x_j$: Quantidade de bobinas grandes cortadas utilizando o padrão $j$.
- $y_j$: Variável binária que assume o valor $1$ se o padrão $j$ for utilizado ($x_j > 0$), e $0$ caso contrário.

**Função Objetivo:** Minimizar o total de bobinas grandes utilizadas
$$\min Z = \sum_{j \in J} x_j$$
**Restrições:**
1. Atender a demanda de cada tipo de corte $i$:
$$\sum_{j = 1}^P Q_{ji} \ x_j = D_i \  \quad i = 1,\ 2,\ ...,\ n$$

2. As quantidades de bobinas cortadas devem ser números inteiros não negativos:
$$x_j \in \mathbb{Z}_+ \quad$$


**Problema b): Limitando o número de padrões de corte a $m_{max}$**

3. Se uma quantidade for produzida no padrão $j$ ($x_j > 0$), a sua variável binária correspondente $y_j$ será obrigatoriamente ligada ($1$):
$$x_j \le M \cdot y_j \quad \forall j \in J$$
4. Limitar o número total de padrões de corte utilizados na fábrica ao valor máximo permitido ($m_{max}$):
$$\sum_{j \in J} y_j \le m_{max}$$
5. Domínio da variável de ativação:

$$y_j \in \{0, 1\} \quad \forall j \in J$$
