def generate_recommendation(
    ai_status,
    haz_status,
    waz_status,
    whz_status
):

    recommendations = []

    if ai_status == "Stunted":
        recommendations.append(
            "Perlu pemantauan pertumbuhan secara berkala karena terindikasi stunting."
        )

    if haz_status == "Stunted":
        recommendations.append(
            "Tinggi badan menurut umur berada di bawah standar WHO."
        )

    if waz_status == "Underweight":
        recommendations.append(
            "Berat badan menurut umur berada di bawah standar WHO."
        )

    if whz_status == "Wasted":
        recommendations.append(
            "Berat badan menurut tinggi badan menunjukkan kondisi kurus."
        )

    if len(recommendations) == 0:
        recommendations.append(
            "Pertumbuhan anak berada dalam rentang normal berdasarkan standar WHO."
        )

    recommendations.append(
        "Lakukan pemantauan rutin di Posyandu atau fasilitas kesehatan."
    )

    recommendations.append(
        "Berikan makanan bergizi seimbang sesuai usia anak."
    )

    return recommendations