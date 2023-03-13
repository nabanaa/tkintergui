def dodaj_pkt(self, x=generuj_sinusa()[0], y=x=


    generuj_sinusa()[1]):
self.start_but["state"] = "disabled"
for k in range(100):
    for u in range(120):
        czas = self.scatter0.get_offsets()[:, 0].tolist()
        self.wartosci_kinetyczna = self.scatter0.get_offsets()[:, 1].tolist()
        self.wartosci_potencjalna = self.scatter1.get_offsets()[:, 1].tolist()
        if len(czas) == 0:
            czas.append(0)
        else:
            czas.append(time.time() - self.__xtimer)
        zmi = np.sin(time.time() * 7)
        self.wartosci_kinetyczna.append(zmi)
        self.wartosci_potencjalna.append(-zmi)
        xx = np.c_[czas, self.wartosci_kinetyczna]
        yy = np.c_[czas, self.wartosci_potencjalna]
        self.scatter0.set_offsets(xx)
        self.scatter1.set_offsets(yy)

        self.axs[0].set_xlim(czas[-1] - 3, czas[-1] + 1)
        self.axs[1].set_xlim(czas[-1] - 3, czas[-1] + 1)
    self.wartosci_potencjalna = self.wartosci_potencjalna[11:]
    czas = czas[11:]
    self.wartosci_kinetyczna = self.wartosci_kinetyczna[11:]

    self.canvas.draw()
