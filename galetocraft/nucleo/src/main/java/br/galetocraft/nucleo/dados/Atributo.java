package br.galetocraft.nucleo.dados;

/** Os seis atributos de um Cocorídeo, com a chave usada na base vigente. */
public enum Atributo {
	HP("HP"), ATAQUE_FISICO("Ataque Físico"), DEFESA_FISICA("Defesa Física"),
	ATAQUE_MAGICO("Ataque Mágico"), DEFESA_MAGICA("Defesa Mágica"), VELOCIDADE("Velocidade");

	private final String chave;

	Atributo(String chave) {
		this.chave = chave;
	}

	public String chave() {
		return chave;
	}
}
