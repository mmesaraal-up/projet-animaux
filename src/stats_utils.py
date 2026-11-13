def analyser_ventes(transactions):
    """Analyse une liste de montants de ventes (en euros)."""
    #  valeurs négatives ou nulles
    valides = [t for t in transactions if t > 0]
    if not valides:
        return {"erreur": "Aucune transaction valide"}

    nombre = len(valides)
    total = sum(valides)
    moyenne = total / nombre

    # Médiane
    triees = sorted(valides)
    milieu = nombre // 2
    if nombre % 2 == 0:
        mediane = (triees[milieu - 1] + triees[milieu]) / 2
    else:
        mediane = triees[milieu]

    # Écart-type 
    variance = sum((t - moyenne) ** 2 for t in valides) / nombre
    ecart_type = variance ** 0.5

    # transactions supérieures à 2 fois la moyenne
    anomalies = [t for t in valides if t > 2 * moyenne]

    return {
        "nombre": nombre,
        "total": total,
        "moyenne": round(moyenne, 2),
        "mediane": mediane,
        "ecart_type": round(ecart_type, 2),
        "max": max(valides),
        "min": min(valides),
        "anomalies": anomalies,
    }


if __name__ == "__main__":
    ventes_test = [150, 200, -50, 0, 320, 180, 2500, 210, 95]
    rapport = analyser_ventes(ventes_test)
    print("=== Rapport statistique des ventes ===")
    for cle, valeur in rapport.items():
        print(f"{cle:<12}: {valeur}")