from datetime import datetime, date
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

class StudyPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StudyPace - Planificateur de révisions")
        self.root.geometry("600x500")
        self.root.config(bg="#f4f6f9")

        self.filename = "schedule_data.json"
        self.subjects = self.load_data()

        # --- HEADER ---
        title_label = tk.Label(root, text="StudyPace", font=("Arial", 18, "bold"), bg="#f4f6f9", fg="#2c3e50")
        title_label.pack(pady=10)

        subtitle_label = tk.Label(root, text="Organise tes révisions et réussis tes examens", font=("Arial", 10), bg="#f4f6f9", fg="#7f8c8d")
        subtitle_label.pack(pady=0)

        # --- FORMULAIRE D'AJOUT ---
        form_frame = tk.LabelFrame(root, text=" Ajouter une matière ", font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#34495e", padx=15, pady=15)
        form_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(form_frame, text="Matière :", bg="#f4f6f9").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(form_frame, width=25)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Difficulté (1-5) :", bg="#f4f6f9").grid(row=1, column=0, sticky="w", pady=5)
        self.diff_spin = ttk.Spinbox(form_frame, from_=1, to=5, width=5, state="readonly")
        self.diff_spin.set(3)
        self.diff_spin.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        tk.Label(form_frame, text="Date d'examen (AAAA-MM-JJ) :", bg="#f4f6f9").grid(row=2, column=0, sticky="w", pady=5)
        self.date_entry = tk.Entry(form_frame, width=25)
        self.date_entry.grid(row=2, column=1, padx=10, pady=5)

        add_btn = tk.Button(form_frame, text="Ajouter au planning", bg="#27ae60", fg="white", font=("Arial", 9, "bold"), command=self.add_subject)
        add_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # --- LISTE DES MATIÈRES / PLAN ---
        list_frame = tk.LabelFrame(root, text=" Ton Programme de Révision Prioritaire ", font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#34495e", padx=15, pady=15)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(list_frame, columns=("Matiere", "Difficulte", "Echeance", "Jours"), show="headings", height=5)
        self.tree.heading("Matiere", text="Matière")
        self.tree.heading("Difficulte", text="Difficulté")
        self.tree.heading("Echeance", text="Date d'examen")
        self.tree.heading("Jours", text="Jours restants")
        
        self.tree.column("Matiere", width=150)
        self.tree.column("Difficulte", width=70, anchor="center")
        self.tree.column("Echeance", width=100, anchor="center")
        self.tree.column("Jours", width=90, anchor="center")
        
        self.tree.pack(fill="both", expand=True)

        self.refresh_list()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_data(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.subjects, f, indent=4, ensure_ascii=False)

    def add_subject(self):
        name = self.name_entry.get().strip()
        difficulty = self.diff_spin.get()
        exam_date_str = self.date_entry.get().strip()

        if not name or not exam_date_str:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis !")
            return

        try:
            exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
            today = date.today()
            days_left = (exam_date - today).days

            if days_left < 0:
                messagebox.showerror("Erreur", "La date de l'examen est déjà passée !")
                return

            subject = {
                "name": name,
                "difficulty": int(difficulty),
                "exam_date": exam_date_str,
                "days_left": days_left
            }
            self.subjects.append(subject)
            self.save_data()
            self.refresh_list()

            # Vider les champs
            self.name_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            messagebox.showinfo("Succès", f"Matière '{name}' ajoutée avec succès !")
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez AAAA-MM-JJ (ex: 2026-10-15).")

    def refresh_listfor_tree(self):
        pass

    def refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Trier par urgence et difficulté
        sorted_subjects = sorted(self.subjects, key=lambda x: (x['days_left'], -x['difficulty']))

        for sub in sorted_subjects:
            self.tree.insert("", "end", values=(sub["name"], f"{sub['difficulty']}/5", sub["exam_date"], f"{sub['days_left']} j"))

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyPlannerApp(root)
    root.mainloop()