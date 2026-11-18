package br.galetocraft.nucleo.dados;

/** Categoria do golpe. Só físico e mágico causam dano direto pela fórmula V5.6. */
public enum Categoria {
	FISICO, MAGICO, SUPORTE, CURA, CONTRA_ATAQUE, SUPORTE_CURA, SUPORTE_CONTRA_ATAQUE;

	public boolean danoDireto() {
		return this == FISICO || this == MAGICO;
	}

	public Atributo ataque() {
		return this == FISICO ? Atributo.ATAQUE_FISICO : Atributo.ATAQUE_MAGICO;
	}

	public Atributo defesa() {
		return this == FISICO ? Atributo.DEFESA_FISICA : Atributo.DEFESA_MAGICA;
	}

	public static Categoria deTexto(String texto) {
		if (texto == null)
			throw new IllegalArgumentException("Golpe sem categoria");
		return switch (Elemento.normalizar(texto)) {
			case "fisico" -> FISICO;
			case "magico" -> MAGICO;
			case "suporte" -> SUPORTE;
			case "cura" -> CURA;
			case "contra-ataque" -> CONTRA_ATAQUE;
			case "suporte/cura" -> SUPORTE_CURA;
			case "suporte/contra-ataque" -> SUPORTE_CONTRA_ATAQUE;
			default -> throw new IllegalArgumentException("Categoria desconhecida: " + texto);
		};
	}
}
