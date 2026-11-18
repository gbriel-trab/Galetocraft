package br.galetocraft.nucleo.dados;

import java.text.Normalizer;
import java.util.Locale;

/** Elementos do Galetocraft: os seis básicos, o Nexo (exclusivo do #023) e os golpes sem eficácia elemental. */
public enum Elemento {
	FOGO("Fogo"), AGUA("Água"), PLANTA("Planta"), TERRA("Terra"), AR("Ar"), ELETRICO("Elétrico"),
	/** Elemento exclusivo do #023 Quetzacocó (Nexo V2.0). */
	NEXO("Nexo"),
	/** Golpe ofensivo sem elemento: multiplicador 1×. */
	NEUTRO("Neutro"),
	/** Suporte e golpes sem elemento: não aplicam eficácia. */
	SEM_ELEMENTO("Sem elemento");

	private final String nome;

	Elemento(String nome) {
		this.nome = nome;
	}

	public String nome() {
		return nome;
	}

	/** Os seis elementos da matriz 6×6. */
	public boolean basico() {
		return ordinal() <= ELETRICO.ordinal();
	}

	/** Participa do cálculo de eficácia (básicos e Nexo). */
	public boolean temEficacia() {
		return basico() || this == NEXO;
	}

	public static Elemento deTexto(String texto) {
		if (texto == null || texto.isBlank())
			return SEM_ELEMENTO;
		String chave = normalizar(texto);
		if (chave.startsWith("neutro"))
			return NEUTRO;   // inclui "Neutro/sem elemento"
		for (Elemento e : values())
			if (normalizar(e.nome).equals(chave))
				return e;
		throw new IllegalArgumentException("Elemento desconhecido: " + texto);
	}

	static String normalizar(String s) {
		return Normalizer.normalize(s, Normalizer.Form.NFD).replaceAll("\\p{M}", "").toLowerCase(Locale.ROOT).trim();
	}
}
