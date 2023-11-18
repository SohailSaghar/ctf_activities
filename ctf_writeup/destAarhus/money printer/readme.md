## Description

File: [money_printer](./money_printer)

## Start

Først finder vi den decompileret kode gennem ghidra. 

![decompiled.png](./decompiled.png)

Dernæst ser vi hvad der var inde i menu item 2 som er der hvor vi kan købe flaget når programmet køres

![secondoption.png](./secondoption.png)

Nu prøver vi at se hvordan koden til purchase item ser ud

![purchaseitem.png](./purchaseitem.png)

Der er noget kondition på vores penge som ser om vi har nok til at kunne købe det ønsket produkt. Vi kan nu patche dette ved at bruge JZ i stedet

![patchtojz.png](./patchtojz.png)

Nu exporterer vi og prøver at købe flaget.

![flag.png](./flag.png)

Flaget er `HKN{E23avvvkrjwavtsxjezgj}`

