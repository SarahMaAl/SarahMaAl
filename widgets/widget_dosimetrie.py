#!/usr/bin/env python3
"""Widget post-it pour calculer des niveaux de dose en dosimétrie."""

import tkinter as tk
from tkinter import messagebox

PERCENTAGES = [10, 50, 95, 98, 100, 105, 107]


class DoseWidget:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Post-it Dosimétrie")
        self.root.geometry("420x560")
        self.root.configure(bg="#fff7b2")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)

        self.prescription_entries: list[tk.Entry] = []

        self._build_header()
        self._build_input_section()
        self._build_output_section()

    def _build_header(self) -> None:
        header = tk.Label(
            self.root,
            text="🩺 Widget Dosimétrie",
            font=("Arial", 16, "bold"),
            bg="#fff7b2",
            fg="#333333",
        )
        header.pack(pady=(10, 4))

        subtitle = tk.Label(
            self.root,
            text="Toujours visible pendant la planification",
            font=("Arial", 10),
            bg="#fff7b2",
            fg="#555555",
        )
        subtitle.pack(pady=(0, 12))

    def _build_input_section(self) -> None:
        input_frame = tk.Frame(self.root, bg="#fff7b2")
        input_frame.pack(fill="x", padx=16)

        tk.Label(
            input_frame,
            text="Nombre de niveaux de dose :",
            bg="#fff7b2",
            font=("Arial", 11, "bold"),
        ).pack(anchor="w")

        levels_row = tk.Frame(input_frame, bg="#fff7b2")
        levels_row.pack(fill="x", pady=(4, 8))

        self.levels_entry = tk.Entry(levels_row, width=8, font=("Arial", 11))
        self.levels_entry.pack(side="left")

        generate_btn = tk.Button(
            levels_row,
            text="Créer champs",
            command=self.generate_prescription_inputs,
            bg="#f8e473",
            activebackground="#f2dc59",
            relief="flat",
            padx=8,
        )
        generate_btn.pack(side="left", padx=8)

        self.prescriptions_frame = tk.Frame(input_frame, bg="#fff7b2")
        self.prescriptions_frame.pack(fill="x")

        self.calculate_btn = tk.Button(
            input_frame,
            text="Calculer",
            command=self.calculate,
            state="disabled",
            bg="#f8e473",
            activebackground="#f2dc59",
            relief="flat",
            padx=10,
        )
        self.calculate_btn.pack(pady=(10, 4), anchor="w")

    def _build_output_section(self) -> None:
        tk.Label(
            self.root,
            text="Résultats (Gy)",
            bg="#fff7b2",
            font=("Arial", 11, "bold"),
        ).pack(anchor="w", padx=16, pady=(10, 4))

        self.output = tk.Text(
            self.root,
            height=18,
            width=48,
            wrap="word",
            font=("Consolas", 10),
            bg="#fffde7",
            relief="flat",
        )
        self.output.pack(fill="both", expand=True, padx=16, pady=(0, 12))

    def generate_prescription_inputs(self) -> None:
        for widget in self.prescriptions_frame.winfo_children():
            widget.destroy()
        self.prescription_entries.clear()

        levels_raw = self.levels_entry.get().strip()
        try:
            levels = int(levels_raw)
            if levels <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Entrez un nombre entier de niveaux > 0.")
            self.calculate_btn.config(state="disabled")
            return

        for i in range(levels):
            row = tk.Frame(self.prescriptions_frame, bg="#fff7b2")
            row.pack(fill="x", pady=2)

            tk.Label(
                row,
                text=f"Prescription niveau {i + 1} (Gy) :",
                bg="#fff7b2",
                font=("Arial", 10),
            ).pack(side="left")

            entry = tk.Entry(row, width=10, font=("Arial", 10))
            entry.pack(side="right")
            self.prescription_entries.append(entry)

        self.calculate_btn.config(state="normal")

    def calculate(self) -> None:
        prescriptions: list[float] = []
        for i, entry in enumerate(self.prescription_entries, start=1):
            value_raw = entry.get().strip().replace(",", ".")
            try:
                value = float(value_raw)
                if value <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Erreur",
                    f"Prescription invalide pour le niveau {i}. Entrez une valeur > 0.",
                )
                return
            prescriptions.append(value)

        self.output.delete("1.0", tk.END)
        for i, prescription in enumerate(prescriptions, start=1):
            self.output.insert(tk.END, f"Niveau {i} - Prescription: {prescription:.2f} Gy\n")
            for percentage in PERCENTAGES:
                result = prescription * (percentage / 100)
                self.output.insert(tk.END, f"  {percentage:>3}% = {result:>7.2f} Gy\n")
            self.output.insert(tk.END, "\n")


def main() -> None:
    root = tk.Tk()
    DoseWidget(root)
    root.mainloop()


if __name__ == "__main__":
    main()
