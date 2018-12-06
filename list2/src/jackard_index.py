class Jackard:

    @staticmethod
    def jackard_for_sentences(good_sentence: str,
                              test_sentence: str) -> int:
        good_tokens, test_tokens = good_sentence.split(), test_sentence.split()

        good_predecesors = ['<BOS>'] + good_tokens
        test_predecesors = ['<BOS>'] + test_tokens

        good_successors = good_tokens + ['<EOS>']
        test_successors = test_tokens + ['<EOS>']

        good_bigrams = set(zip(good_predecesors, good_successors))
        test_bigrams = set(zip(test_predecesors, test_successors))

        # Calculate intersection and sum
        n_common_bigrams = len(good_bigrams.intersection(test_bigrams))
        n_bigrams = len(good_bigrams)

        # Final calc
        jackard_index = n_common_bigrams / n_bigrams

        return jackard_index
