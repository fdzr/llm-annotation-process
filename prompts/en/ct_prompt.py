BASE_PROMPT = {
    "role": "system",
    "content": """ You will be provided with pair of sentences, and you task is to annotate pair of sentences
    based on a common target word that appears in both sentences and the target word may be in a different
    grammatical form that derives from the lemma of the original target word. You will annotate the sentences
    with 1 or 2 or 3 or 4 where:
    
    1 means that the meaning of the target word in both sentences is completely different or unrelated.
    2 means that the meaning of the target word in both sentences is distantly related
    3 means that the meaning of the target word in both sentences is closely related
    4 means that the meaning of the target word in both sentences are identical

    Example:
        target word: planta
        Sentence 1: Las plantas sembradas en el jardin, brotan un inmenso aroma.
        Sentence 2: Las plantas de carbon son capaces de generar energia electrica
                    para toda una ciudad

        Score: 1, in this case the annotation is 1 because in the first sentence planta is related
            to trees, flowers and the sentence planta is related to factories, the meaning is
            completely unrelated

    Example:
        target word: arbol
        Sentence 1: Un arbol binario es una estructura de datos para almacenas datos organizados.
        Sentence 2: Los arboles de ese bosque son ricos en aroma y colores.
        
        Score: 2, in this case the annotation is 2 because in the first sentence arbol means a data structure and
        in the second sentence arboles mean the plant that have leaves, the meaning is distantly related
        because they share the form of a tree but in one case is a data structure and in the second sentence
        is a tree.

    Example: 
        target word: celda
        Sentence 1: Con este conocido programa podremos manipular los datos a traves de sus celdas.
        Sentence 2: Como resultados de dicho analisis vamos a obtener un mapa diferente, un mapa
                    donde cada celda visible nos viene con un numero de 0 o 180 grados.

        Score: 3, in this case the annotation is 3 because in the first sentence the meaning of celda is
            related to squares where you can put information and in the second sentence the meanig is related also
            to squares where you can gather information, it is not 4 because the meanings differ that it is used
            in a program and the other one is used in a map

    Example:
        target word: caballo
        Sentence 1: El caballo blanco de Marti galopa sin parar hasta la victoria.
        Sentence 2: Los caballos cuando estan en manada se protegen los unos a los otros.

        Score: 4, in this case, the annotation is 4 because in both sentences, the meaning of
            caballo y caballos is related to the animal. Please note that caballo is singular and caballos
            is plural do not affect the annotation.

    - The answer you will provide must contain only the score.
    - Never justify your choice.

    Target word: {target_word}
    Sentence 1: {sentence1}
    Sentence 2: {sentence2}

""",
}
