from num2words import num2words


def num_extenso_formatado(valor: float):
    parte_inteira = int(valor)
    parte_decimal = round((valor - parte_inteira) * 100)
        
    valor_formatado = f"{parte_inteira:,}".replace(",", ".") + f",{parte_decimal:02d}"
    parte_inteira_extenso = num2words(parte_inteira, lang="pt_BR")
    parte_decimal_extenso = num2words(parte_decimal, lang="pt_BR")
        
    return valor_formatado, parte_inteira_extenso, parte_decimal_extenso


