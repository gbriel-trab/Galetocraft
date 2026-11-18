package br.galetocraft.nucleo.dados;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Catálogo vigente: espécies, golpes e regras exportados da base (ferramentas/base/exportar_para_mod.py).
 * Os arquivos ficam no classpath em {@code /galetocraft/dados/}.
 */
public final class Galetario {
	private static final String PASTA = "/galetocraft/dados/";
	private static volatile Galetario padrao;

	private final Map<Integer, Especie> especies;
	private final Map<String, JsonElement> regras;
	private final int revisaoBase;

	private Galetario(Map<Integer, Especie> especies, Map<String, JsonElement> regras, int revisaoBase) {
		this.especies = Collections.unmodifiableMap(especies);
		this.regras = Collections.unmodifiableMap(regras);
		this.revisaoBase = revisaoBase;
	}

	/** Catálogo embutido no jar (carregado uma vez). */
	public static Galetario padrao() {
		if (padrao == null) {
			synchronized (Galetario.class) {
				if (padrao == null)
					padrao = carregar(Galetario.class);
			}
		}
		return padrao;
	}

	public static Galetario carregar(Class<?> origem) {
		JsonArray especiesJson = ler(origem, "especies.json").getAsJsonArray();
		JsonObject regrasJson = ler(origem, "regras.json").getAsJsonObject();
		JsonObject versao = ler(origem, "versao.json").getAsJsonObject();
		Map<Integer, Especie> especies = new LinkedHashMap<>();
		for (JsonElement e : especiesJson) {
			Especie s = especie(e.getAsJsonObject());
			especies.put(s.numero(), s);
		}
		Map<String, JsonElement> regras = new LinkedHashMap<>();
		regrasJson.entrySet().forEach(r -> regras.put(r.getKey(), r.getValue()));
		return new Galetario(especies, regras, versao.get("revisao_base").getAsInt());
	}

	private static JsonElement ler(Class<?> origem, String arquivo) {
		try (InputStream in = origem.getResourceAsStream(PASTA + arquivo)) {
			if (in == null)
				throw new IllegalStateException("Dados do Galetário ausentes: " + PASTA + arquivo);
			try (Reader r = new InputStreamReader(in, StandardCharsets.UTF_8)) {
				return JsonParser.parseReader(r);
			}
		} catch (IOException ex) {
			throw new IllegalStateException("Falha ao ler " + arquivo, ex);
		}
	}

	private static Especie especie(JsonObject o) {
		Map<Atributo, Integer> atributos = new EnumMap<>(Atributo.class);
		JsonObject a = o.getAsJsonObject("atributos");
		for (Atributo at : Atributo.values())
			atributos.put(at, a.get(at.chave()).getAsInt());
		List<Elemento> elementos = new ArrayList<>();
		o.getAsJsonArray("elementos").forEach(e -> elementos.add(Elemento.deTexto(e.getAsString())));
		List<String> alas = new ArrayList<>();
		Double machos = null;
		if (o.has("galeria") && o.get("galeria").isJsonObject()) {
			JsonObject g = o.getAsJsonObject("galeria");
			g.getAsJsonArray("alas").forEach(x -> alas.add(x.getAsString()));
			machos = g.get("probabilidade_macho").getAsDouble();
		}
		List<Golpe> golpes = new ArrayList<>();
		o.getAsJsonArray("golpes").forEach(g -> golpes.add(golpe(g.getAsJsonObject())));
		return new Especie(o.get("numero").getAsInt(), o.get("nome").getAsString(), o.get("raridade").getAsString(),
				List.copyOf(elementos), Collections.unmodifiableMap(atributos), o.get("peso_kg").getAsDouble(),
				texto(o.getAsJsonObject("passiva"), "nome"), List.copyOf(alas), machos, texto(o, "hereditario"), List.copyOf(golpes));
	}

	private static Golpe golpe(JsonObject g) {
		EstadoNegativo estado = null;
		double chance = 0;
		if (g.has("aplica_estado") && g.get("aplica_estado").isJsonObject()) {
			JsonObject ae = g.getAsJsonObject("aplica_estado");
			estado = EstadoNegativo.deTexto(ae.get("estado").getAsString());
			chance = ae.get("chance").getAsDouble();
		}
		JsonObject estruturado = g.has("efeito_estruturado") && g.get("efeito_estruturado").isJsonObject()
				? g.getAsJsonObject("efeito_estruturado") : null;
		return new Golpe(g.get("grupo").getAsString(), g.get("posicao").getAsInt(), g.get("nome").getAsString(), texto(g, "id"),
				Elemento.deTexto(texto(g, "elemento")), Categoria.deTexto(texto(g, "categoria")), inteiro(g, "poder"),
				texto(g, "poder_texto"), inteiro(g, "energia") == null ? 0 : inteiro(g, "energia"), texto(g, "efeito"),
				estado, chance, estruturado);
	}

	private static String texto(JsonObject o, String campo) {
		return o.has(campo) && !o.get(campo).isJsonNull() ? o.get(campo).getAsString() : null;
	}

	private static Integer inteiro(JsonObject o, String campo) {
		return o.has(campo) && !o.get(campo).isJsonNull() ? o.get(campo).getAsInt() : null;
	}

	public int revisaoBase() {
		return revisaoBase;
	}

	public List<Especie> especies() {
		return List.copyOf(especies.values());
	}

	public Especie especie(int numero) {
		Especie e = especies.get(numero);
		if (e == null)
			throw new IllegalArgumentException("Espécie inexistente: #" + numero);
		return e;
	}

	public Optional<Especie> especie(String nome) {
		String chave = Elemento.normalizar(nome);
		return especies.values().stream().filter(e -> Elemento.normalizar(e.nome()).equals(chave)).findFirst();
	}

	/** Conteúdo de uma regra de current_rules (ex.: "dano_v5_6", "climas", "captura"). */
	public JsonElement regra(String id) {
		JsonElement r = regras.get(id);
		if (r == null)
			throw new IllegalArgumentException("Regra inexistente na base: " + id);
		return r;
	}

	public JsonObject regraObjeto(String id) {
		return regra(id).getAsJsonObject();
	}
}
