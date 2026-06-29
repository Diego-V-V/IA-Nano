"""
RAG (Retrieval-Augmented Generation) para el Sistema SEM Multi-Agente.
Base de conocimiento con referencias bibliográficas reales indexadas en ChromaDB.
"""
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any

# ── Cliente ChromaDB en memoria ──────────────────────────────
chroma_client = chromadb.EphemeralClient()
default_ef = embedding_functions.DefaultEmbeddingFunction()

collection = chroma_client.get_or_create_collection(
    name="sem_scientific_literature",
    embedding_function=default_ef,
)

# ══════════════════════════════════════════════════════════════
# BASE DE CONOCIMIENTO CON REFERENCIAS BIBLIOGRÁFICAS REALES
# ══════════════════════════════════════════════════════════════
# Cada entrada contiene: contenido científico + referencia (autor, revista, año, DOI)

LITERATURA_SEM = [
    # ── TiO2 ──────────────────────────────────────────────────
    {
        "text": (
            "TiO2 nanoparticles in the anatase phase exhibit a band gap of ~3.2 eV and "
            "high photocatalytic activity for degradation of organic pollutants under UV light. "
            "Particle sizes below 25 nm show quantum confinement effects that widen the band gap, "
            "increasing redox potential. Surface area increases inversely with particle size, "
            "reaching >200 m²/g for sub-10 nm particles. "
            "Applications: photocatalytic water splitting, self-cleaning coatings, dye-sensitized solar cells (DSSC), "
            "UV filters in sunscreens, and antimicrobial surfaces."
        ),
        "ref": "Chen, X. & Mao, S.S. (2007). Titanium Dioxide Nanomaterials: Synthesis, Properties, Modifications, and Applications. Chemical Reviews, 107(7), 2891-2959. DOI: 10.1021/cr0500535",
        "compound": "TiO2",
        "morphology": "nanoparticles",
    },
    {
        "text": (
            "TiO2 nanowires (1D) grown via hydrothermal synthesis show lengths of 1-10 μm "
            "and diameters of 20-200 nm. Their 1D morphology provides direct electron transport "
            "pathways, reducing charge recombination by up to 10x compared to nanoparticle films. "
            "Rutile nanowires on FTO substrates achieve solar-to-hydrogen efficiencies of ~1.5% "
            "in photoelectrochemical cells. "
            "Applications: photoelectrochemical water splitting, perovskite solar cell scaffolds, "
            "lithium-ion battery anodes, gas sensors (NO2, ethanol)."
        ),
        "ref": "Liu, B. & Aydil, E.S. (2009). Growth of Oriented Single-Crystalline Rutile TiO2 Nanorods on Transparent Conducting Substrates for Dye-Sensitized Solar Cells. J. Am. Chem. Soc., 131(11), 3985-3990. DOI: 10.1021/ja8078972",
        "compound": "TiO2",
        "morphology": "nanowires",
    },

    # ── ZnO ──────────────────────────────────────────────────
    {
        "text": (
            "ZnO nanoparticles (wurtzite, Eg ~3.37 eV) with diameters of 20-100 nm exhibit "
            "strong UV absorption, making them ideal for UV-blocking applications. "
            "Below 10 nm, blue-shifted photoluminescence is observed due to quantum confinement. "
            "ZnO NPs generate reactive oxygen species (ROS) upon UV excitation, providing "
            "potent antibacterial activity against E. coli and S. aureus. "
            "Applications: UV protection in cosmetics, antibacterial coatings, "
            "varistors, transparent conductive films, photocatalysis."
        ),
        "ref": "Klingshirn, C. (2007). ZnO: From Basics Towards Applications. Physica Status Solidi (b), 244(9), 3027-3073. DOI: 10.1002/pssb.200743072",
        "compound": "ZnO",
        "morphology": "nanoparticles",
    },
    {
        "text": (
            "ZnO nanowires synthesized by vapor-liquid-solid (VLS) or hydrothermal methods "
            "typically have diameters of 50-200 nm and lengths up to 10 μm. "
            "Their piezoelectric coefficient d33 ~12.4 pm/V enables energy harvesting from "
            "mechanical vibrations. Single ZnO nanowire FETs show electron mobilities "
            "of 75 cm²/V·s. Wang et al. demonstrated the first piezoelectric nanogenerator "
            "using ZnO nanowire arrays. "
            "Applications: piezoelectric nanogenerators, UV nano-lasers, "
            "field-emission displays, chemical/gas sensors, biosensors."
        ),
        "ref": "Wang, Z.L. & Song, J. (2006). Piezoelectric Nanogenerators Based on Zinc Oxide Nanowire Arrays. Science, 312(5771), 242-246. DOI: 10.1126/science.1124005",
        "compound": "ZnO",
        "morphology": "nanowires",
    },

    # ── Au (Gold) ─────────────────────────────────────────────
    {
        "text": (
            "Gold nanoparticles (Au NPs) exhibit localized surface plasmon resonance (LSPR) "
            "that is strongly size-dependent: 10 nm NPs absorb at ~520 nm (green-blue); "
            "50 nm at ~530 nm; 100 nm at ~570 nm with significant scattering contribution. "
            "Molar extinction coefficients reach 10^8-10^11 M⁻¹cm⁻¹, orders of magnitude "
            "higher than organic dyes. Biocompatibility enables in vivo applications. "
            "Applications: colorimetric biosensors, lateral flow assays (pregnancy tests), "
            "photothermal cancer therapy, SERS substrates, drug delivery vehicles, "
            "catalysis (CO oxidation at low temperature)."
        ),
        "ref": "Daniel, M.C. & Astruc, D. (2004). Gold Nanoparticles: Assembly, Supramolecular Chemistry, Quantum-Size-Related Properties, and Applications toward Biology, Catalysis, and Nanotechnology. Chemical Reviews, 104(1), 293-346. DOI: 10.1021/cr030698+",
        "compound": "Au",
        "morphology": "nanoparticles",
    },
    {
        "text": (
            "Gold nanowires (Au NWs) with diameters <50 nm and aspect ratios >1000 "
            "exhibit ballistic electron transport and resistivities approaching bulk gold "
            "(2.2 μΩ·cm). Ultrathin Au nanowires (<2 nm diameter) show quantized conductance. "
            "Nanowire networks form transparent conductive films with sheet resistance "
            "<30 Ω/sq at >85% transmittance. "
            "Applications: flexible transparent electrodes, interconnects in nanoelectronics, "
            "molecular electronics, SERS-active substrates, stretchable sensors."
        ),
        "ref": "Halder, A. & Ravishankar, N. (2007). Ultrafine Single-Crystalline Gold Nanowire Arrays by Oriented Attachment. Advanced Materials, 19(14), 1854-1858. DOI: 10.1002/adma.200602325",
        "compound": "Au",
        "morphology": "nanowires",
    },

    # ── Ag (Silver) ───────────────────────────────────────────
    {
        "text": (
            "Silver nanoparticles (Ag NPs) show the strongest LSPR of all plasmonic metals, "
            "with extinction coefficients 10x higher than Au NPs at equivalent sizes. "
            "SERS enhancement factors reach 10^6-10^8 on individual Ag NPs. "
            "Ag⁺ ion release provides broad-spectrum antimicrobial activity: MIC values of "
            "10-100 μg/mL against E. coli, S. aureus, and P. aeruginosa. "
            "Size-dependent toxicity: NPs <10 nm show highest antibacterial efficacy. "
            "Applications: wound dressings, water purification, antimicrobial coatings, "
            "SERS-based molecular detection, conductive inks."
        ),
        "ref": "Rai, M., Yadav, A. & Gade, A. (2009). Silver nanoparticles as a new generation of antimicrobials. Biotechnology Advances, 27(1), 76-83. DOI: 10.1016/j.biotechadv.2008.09.002",
        "compound": "Ag",
        "morphology": "nanoparticles",
    },
    {
        "text": (
            "Silver nanowires (Ag NWs) synthesized by polyol method achieve diameters of "
            "30-100 nm, lengths of 10-50 μm, and aspect ratios >500. "
            "Random Ag NW networks on PET substrates achieve sheet resistance <20 Ω/sq "
            "at >90% optical transmittance (at 550 nm), superior to ITO on flexible substrates. "
            "Ag NWs maintain conductivity after >10,000 bending cycles at 5 mm radius. "
            "Applications: flexible transparent electrodes for OLED/LCD, touchscreens, "
            "solar cell front contacts, stretchable heaters, electromagnetic interference shielding."
        ),
        "ref": "Ye, S., Rathmell, A.R., Chen, Z., Stewart, I.E. & Wiley, B.J. (2014). Metal Nanowire Networks: The Next Generation of Transparent Conductors. Advanced Materials, 26(39), 6670-6687. DOI: 10.1002/adma.201402710",
        "compound": "Ag",
        "morphology": "nanowires",
    },

    # ── SiO2 ──────────────────────────────────────────────────
    {
        "text": (
            "SiO2 (silica) nanoparticles synthesized by the Stöber method produce highly "
            "monodisperse spheres (PDI <0.05) with controllable diameters from 50 nm to 2 μm. "
            "Mesoporous SiO2 nanoparticles (MSNs) like MCM-41 have pore sizes of 2-10 nm, "
            "surface areas of 700-1000 m²/g, and pore volumes of ~1 cm³/g. "
            "Biocompatibility and FDA approval for food additives make them attractive for "
            "biomedical use. "
            "Applications: drug delivery (controlled release), bioimaging (fluorescent tagging), "
            "chromatography packing, catalyst supports, thermal insulation (aerogels), "
            "CMP slurries in semiconductor manufacturing."
        ),
        "ref": "Slowing, I.I., Vivero-Escoto, J.L., Wu, C.W. & Lin, V.S.Y. (2008). Mesoporous silica nanoparticles as controlled release drug delivery and gene transfection carriers. Advanced Drug Delivery Reviews, 60(11), 1278-1288. DOI: 10.1016/j.addr.2008.03.012",
        "compound": "SiO2",
        "morphology": "nanoparticles",
    },

    # ── Fe3O4 (Magnetite) ────────────────────────────────────
    {
        "text": (
            "Fe3O4 (magnetite) nanoparticles below 20 nm exhibit superparamagnetic behavior "
            "with saturation magnetization of 50-80 emu/g (vs 92 emu/g bulk). "
            "Surface functionalization with PEG or silica improves colloidal stability and "
            "biocompatibility. T2 relaxivity values of 100-200 mM⁻¹s⁻¹ make them excellent "
            "MRI contrast agents. Specific absorption rates (SAR) of 200-500 W/g enable "
            "magnetic hyperthermia therapy at AC fields of 100-300 kHz. "
            "Applications: MRI contrast agents, magnetic hyperthermia cancer treatment, "
            "targeted drug delivery, magnetic separation, biosensors, "
            "environmental remediation (heavy metal removal)."
        ),
        "ref": "Laurent, S., Forge, D., Port, M., Roch, A., Robic, C., Vander Elst, L. & Muller, R.N. (2008). Magnetic Iron Oxide Nanoparticles: Synthesis, Stabilization, Vectorization, Physicochemical Characterizations, and Biological Applications. Chemical Reviews, 108(6), 2064-2110. DOI: 10.1021/cr068445e",
        "compound": "Fe3O4",
        "morphology": "nanoparticles",
    },

    # ── CuO ───────────────────────────────────────────────────
    {
        "text": (
            "CuO nanoparticles (monoclinic, Eg ~1.2-1.5 eV) with sizes of 10-100 nm "
            "show p-type semiconductor behavior useful for gas sensing. "
            "CuO NPs exhibit catalytic activity for CO oxidation at temperatures as low as 200°C. "
            "Antibacterial mechanism involves Cu²⁺ ion release and ROS generation. "
            "CuO nanowires grown by thermal oxidation of Cu foils achieve diameters of "
            "50-200 nm and lengths up to 15 μm with monoclinic crystal structure. "
            "Applications: gas sensors (H2S, NO2), lithium-ion battery anodes (theoretical "
            "capacity 674 mAh/g), solar cells, catalysis, antimicrobial agents."
        ),
        "ref": "Zhang, Q., Zhang, K., Xu, D., Yang, G., Huang, H., Nie, F., Liu, C. & Yang, S. (2014). CuO nanostructures: Synthesis, characterization, growth mechanisms, fundamental properties, and applications. Progress in Materials Science, 60, 208-337. DOI: 10.1016/j.pmatsci.2013.09.003",
        "compound": "CuO",
        "morphology": "nanoparticles",
    },

    # ── Deep Learning SEM Classification ─────────────────────
    {
        "text": (
            "The NFFA-EUROPE SEM dataset contains 18,577 micrographs in 10 categories, "
            "publicly available for benchmarking ML models on SEM image classification. "
            "Transfer learning with ResNet-18 pretrained on ImageNet achieves >95% accuracy "
            "on binary classification tasks (e.g., particles vs. nanowires) with only "
            "~200-500 training images per class after fine-tuning. "
            "Grad-CAM visualization confirms that CNNs learn physically meaningful features: "
            "activation maps highlight particle boundaries for 0D structures and "
            "elongated edges for 1D structures."
        ),
        "ref": "Aversa, R., Modarres, M.H., Cozzini, S., Ciancio, R. & Cataldo, A. (2018). The first annotated set of scanning electron microscopy images for nanoscience. Scientific Data, 5, 180172. DOI: 10.1038/sdata.2018.172",
        "compound": "general",
        "morphology": "general",
    },

    # ── Size-dependent properties general ─────────────────────
    {
        "text": (
            "General size-property relationships in nanomaterials: (1) Quantum confinement "
            "increases band gap for semiconductors below Bohr exciton radius; "
            "(2) Surface-to-volume ratio scales as 6/d for spherical NPs (d = diameter); "
            "(3) Melting point depression follows Gibbs-Thomson equation, with NPs <5 nm "
            "melting hundreds of degrees below bulk; (4) Catalytic activity typically peaks "
            "at 2-5 nm where fraction of surface atoms exceeds 50%. "
            "1D nanowires offer advantages over 0D NPs in: electron transport (mean free path), "
            "mechanical flexibility, and network formation for percolation-based devices."
        ),
        "ref": "Roduner, E. (2006). Size matters: why nanomaterials are different. Chem. Soc. Rev., 35, 583-592. DOI: 10.1039/b502142c",
        "compound": "general",
        "morphology": "general",
    },

    # ── Carbon-based nanomaterials ────────────────────────────
    {
        "text": (
            "Carbon nanotubes (CNTs) — single-walled (SWCNT, d=0.4-2 nm) and multi-walled "
            "(MWCNT, d=5-100 nm) — exhibit tensile strengths of 11-63 GPa, "
            "Young's modulus of ~1 TPa, thermal conductivity of ~3500 W/m·K, "
            "and current-carrying capacity of 10⁹ A/cm². SWCNTs can be metallic or "
            "semiconducting depending on chirality. "
            "Applications: composite reinforcement, field-emission sources, "
            "AFM/STM probe tips, nanoelectronics (CNT-FETs), chemical sensors, "
            "supercapacitor electrodes, drug delivery carriers."
        ),
        "ref": "De Volder, M.F.L., Tawfick, S.H., Baughman, R.H. & Hart, A.J. (2013). Carbon Nanotubes: Present and Future Commercial Applications. Science, 339(6119), 535-539. DOI: 10.1126/science.1222453",
        "compound": "C",
        "morphology": "nanowires",
    },
]


def initialize_rag():
    """Indexa la literatura en ChromaDB si la colección está vacía."""
    try:
        count = collection.count()
        if count == 0:
            print("[RAG] Indexando base de conocimientos bibliografica en ChromaDB...")
            docs = []
            ids = []
            metadatas = []
            for i, entry in enumerate(LITERATURA_SEM):
                # Combinar texto + referencia para que el embedding capture ambos
                full_text = f"{entry['text']}\n\n[REF] {entry['ref']}"
                docs.append(full_text)
                ids.append(f"ref_{i}")
                metadatas.append({
                    "source": "curated_bibliography",
                    "reference": entry["ref"],
                    "compound": entry["compound"],
                    "morphology": entry["morphology"],
                })

            collection.add(documents=docs, ids=ids, metadatas=metadatas)
            print(f"[RAG] {len(docs)} referencias bibliograficas indexadas correctamente.")
        else:
            print(f"[RAG] Base de datos activa con {count} documentos.")
    except Exception as e:
        print(f"[RAG] Error inicializando RAG ChromaDB: {e}")


def query_rag(query: str, n_results: int = 3) -> str:
    """
    Busca literatura científica relevante por similitud semántica.
    Retorna los fragmentos con sus referencias bibliográficas.
    """
    try:
        count = collection.count()
        if count == 0:
            initialize_rag()
            count = collection.count()

        results = collection.query(
            query_texts=[query],
            n_results=min(n_results, count),
            include=["documents", "metadatas"],
        )

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        if not docs:
            return "No se encontraron referencias bibliográficas relacionadas."

        # Formatear salida con referencias explícitas
        sections = []
        for doc, meta in zip(docs, metas):
            ref = meta.get("reference", "Referencia no disponible")
            sections.append(f"{doc}\nReferencia: {ref}")

        return "\n\n---\n\n".join(sections)
    except Exception as e:
        return f"Error en búsqueda RAG: {e}"


def query_rag_with_metadata(query: str, n_results: int = 3) -> list:
    """
    Retorna resultados RAG como lista de dicts para uso programático.
    """
    try:
        count = collection.count()
        if count == 0:
            initialize_rag()
            count = collection.count()

        results = collection.query(
            query_texts=[query],
            n_results=min(n_results, count),
            include=["documents", "metadatas", "distances"],
        )

        output = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]
        for doc, meta, dist in zip(docs, metas, dists):
            output.append({
                "text": doc,
                "reference": meta.get("reference", ""),
                "compound": meta.get("compound", ""),
                "morphology": meta.get("morphology", ""),
                "distance": float(dist),
            })
        return output
    except Exception as e:
        return []


# Inicializar al importar
initialize_rag()
