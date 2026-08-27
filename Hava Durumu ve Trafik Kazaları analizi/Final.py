import pandas as pd

#  Veri setlerini yükle
weather_df = pd.read_csv(
    r"C:\Users\Kaan\Desktop\Veri madenciliği final\istanbul_weather.csv",
    sep=";",
    usecols=["date", "city", "weather"]
)

accident_df = pd.read_csv(
    r"C:\Users\Kaan\Desktop\Veri madenciliği final\istanbul_accidents.csv",
    sep=";",
    usecols=["date", "city", "accident_count"]
)


# İstanbul ve izmir verileri
cities = ["Istanbul", "Izmir"]

weather_df = weather_df[weather_df["city"].isin(cities)]
accident_df = accident_df[accident_df["city"].isin(cities)]


# Veri setlerini birleştir
merged_df = pd.merge(
    weather_df,
    accident_df,
    on=["date", "city"],
    how="inner"
)

#  Şehir ve hava durumuna göre ORTALAMA kaza sayıları
result = merged_df.groupby(["city", "weather"])["accident_count"].mean()

print("\nŞehir ve Hava Durumuna Göre ORTALAMA Kaza Sayıları:\n")
print(result)



avg_result = merged_df.groupby("weather")["accident_count"].mean()

print("\nHava Durumuna Göre ORTALAMA Trafik Kazası Sayıları:\n")
print(avg_result)


day_counts = merged_df["weather"].value_counts()

print("\nHava Durumuna Göre Gün Sayıları:\n")
print(day_counts)
day_counts_city = merged_df.groupby(["city", "weather"]).size()

print("\nŞehir ve Hava Durumuna Göre Gün Sayıları:\n")
print(day_counts_city)



normalized_result = result / day_counts_city


print("\nŞehir ve Hava Durumuna Göre GÜN BAŞINA KAZA SAYISI:\n")
print(normalized_result)


import matplotlib.pyplot as plt

# Çoklu indeks → DataFrame'e çevir
plot_df = result.reset_index()

plt.figure()
for city in plot_df["city"].unique():
    city_data = plot_df[plot_df["city"] == city]
    plt.bar(
        city_data["weather"] + " - " + city,
        city_data["accident_count"]
    )

plt.xlabel("Hava Durumu - Şehir")
plt.ylabel("Ortalama Kaza Sayısı")
plt.title("Şehir ve Hava Durumuna Göre Ortalama Trafik Kazaları")
plt.show()



norm_df = normalized_result.reset_index()

plt.figure()
for city in norm_df["city"].unique():
    city_data = norm_df[norm_df["city"] == city]
    plt.plot(
        city_data["weather"],
        city_data[0],
        marker='o',
        label=city
    )

plt.xlabel("Hava Durumu")
plt.ylabel("Gün Başına Ortalama Kaza")
plt.title("Hava Koşullarına Göre Gün Başına Trafik Kazaları")
plt.legend()
plt.show()



sunny_df = norm_df[norm_df["weather"] == "Sunny"]

plt.figure()
plt.bar(sunny_df["city"], sunny_df[0])
plt.xlabel("Şehir")
plt.ylabel("Gün Başına Kaza (Sunny)")
plt.title("Güneşli Havada Şehirlere Göre Günlük Kaza Ortalaması")
plt.show()
