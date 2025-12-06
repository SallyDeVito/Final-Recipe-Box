import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod


class Valid(ABC):
    @abstractmethod
    def validate(self, value):
        pass

class NameValid(Valid):
    def validate(self, value):
        if not value.strip():
            return False, "Name cannot be empty"
        return True

class RatingValid(Valid):
    def validate(self, value):
        rating = float(value)
        if 0 <= rating <= 5:
            return True
        elif ValueError:
            False, "Rating must be 0-5"
        elif TypeError:
            return False, "Must be a number"


class Diff(ABC):
    @abstractmethod
    def get_level(self):
        pass

class Easy(Diff):
    def get_level(self):
        return "Easy"

class Medium(Diff):
    def get_level(self):
        return "Medium"

class Hard(Diff):
    def get_level(self):
        return "Hard"

def get_difficulty(rating):    
    if rating <= 1.9:
        return Easy()
    elif rating <= 3.9:
        return Medium()
    else:
        return Hard()

class Recipe:
    def __init__(self, name: str, ingredients: str, rating: float):
        self._name = name
        self._ingredients = ingredients
        self._rating = rating
        self._validate()
    
    def _validate(self):
        validators = [NameValid(), RatingValid()]

        is_valid, error = validators[0].validate(self._name)
        if not is_valid:
            raise ValueError(f"Name: {error}")
        
        is_valid, error = validators[1].validate(str(self._rating))
        if not is_valid:
            raise ValueError(f"Rating: {error}")
    
    @property
    def name(self):
        return self._name
    
    @property
    def ingredients(self):
        return self._ingredients
    
    @property
    def rating(self):
        return self._rating
    
    def get_difficulty(self):
        return get_difficulty(self._rating).get_level()
    
    def get_full_info(self):
        return f"""Recipe: {self._name}
Difficulty: {self.get_difficulty()} ({self._rating}/5)

Ingredients:{self._ingredients}"""

class RecipeManager:
    def __init__(self):
        self._recipes = [] 
    
    def add_recipe(self, recipe: Recipe):
        self._recipes.append(recipe)
    
    def get_all_recipes(self):
        return self._recipes.copy()
    
    def search_recipes(self, search_term: str):
        search_term = search_term.lower()
        results = []
        for recipe in self._recipes:
            if search_term in recipe.name.lower():
                results.append(recipe)
        return results
    
    def get_recipe_count(self):
        return len(self._recipes)

class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Box")
        self.root.geometry("400x300")
        
        self.recipe_manager = RecipeManager()
        tk.Label(root, text="RECIPE BOX").pack(pady=20)
        tk.Button(root, text="Adding a Recipe", command=self.add).pack(pady=10)
        tk.Button(root, text="Find a Recipe", command=self.find).pack(pady=10)
        tk.Button(root, text="Editing a Recipe", command=self.edit).pack(pady=10)
    
    def add(self):
        win = tk.Toplevel(self.root)
        win.title("Add Recipe")
        win.geometry("400x450")

        tk.Label(win, text="Name:").pack(pady=5)
        name_entry = tk.Entry(win, width=30)
        name_entry.pack()
        
        tk.Label(win, text="Recipe:").pack(pady=5)
        recipe_text = tk.Text(win, width=40)
        recipe_text.pack()
        
        tk.Label(win, text="Rating (0-5):").pack(pady=5)
        rating_entry = tk.Entry(win, width=10)
        rating_entry.pack()
        
        def save():
            try:
                recipe = Recipe( name=name_entry.get(), ingredients=recipe_text.get("1.0", tk.END).strip(),rating=float(rating_entry.get()))
                self.recipe_manager.add_recipe(recipe)
                messagebox.showinfo("Success", f"Added: {recipe.name}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(win, text="Save Recipe", command=save).pack(pady=20)
    
    def find(self):
        win = tk.Toplevel(self.root)
        win.title("Find Recipe")
        win.geometry("500x500")
        
        tk.Label(win, text="Search for Recipe:").pack(pady=10)
        search_entry = tk.Entry(win, width=30)
        search_entry.pack()
        
        tk.Label(win, text="Details:").pack(pady=10)
        recipe_display = tk.Text(win, width=55, wrap=tk.WORD)
        recipe_display.pack(pady=5)
        
        def search():
            search_term = search_entry.get().strip()
            recipe_display.delete("1.0", tk.END)
            
            if not search_term:
                recipe_display.insert("1.0", "Please enter a search term")
                return
            
            found_recipes = self.recipe_manager.search_recipes(search_term)
            
            if not found_recipes:
                recipe_display.insert("1.0", f"No recipes found for '{search_term}'")
            elif len(found_recipes) == 1:
                recipe_display.insert("1.0", found_recipes[0].get_full_info())
            else:
                recipe_display.insert("1.0", f"Found {len(found_recipes)} recipes:\n\n")
                for i, recipe in enumerate(found_recipes, 1):
                    recipe_display.insert(tk.END, f"{i}. {recipe.name}\n")
        
        tk.Button(win, text="Search", command=search).pack(pady=10)
    
    def edit(self):
        if self.recipe_manager.get_recipe_count() == 0:
            messagebox.showinfo("Info", "No recipes to edit")
            return
        
        win = tk.Toplevel(self.root)
        win.title("Edit Recipe")
        win.geometry("400x400")
        
        tk.Label(win, text="Select to edit:").pack(pady=10)
        
        # Use a listbox for selection
        listbox = tk.Listbox(win, width=40, height=10)
        listbox.pack(pady=10)
        
        all_recipes = self.recipe_manager.get_all_recipes()
        for recipe in all_recipes:
            listbox.insert(tk.END, recipe.name)
        
        def open_edit():
            selection = listbox.curselection()
            if not selection:
                messagebox.showinfo("Info", "Please select a recipe")
                return
            
            index = selection[0]
            self._edit_recipe(index, win)
        
        tk.Button(win, text="Edit Selected", command=open_edit).pack(pady=10)
    
    def _edit_recipe(self, index: int, parent_window):
        recipe = self.recipe_manager.get_all_recipes()[index]
        
        win = tk.Toplevel(parent_window)
        win.title(f"Edit {recipe.name}")
        win.geometry("400x450")
        
        tk.Label(win, text="Name:").pack(pady=5)
        name_entry = tk.Entry(win, width=30)
        name_entry.insert(0, recipe.name)
        name_entry.pack()
        
        tk.Label(win, text="Recipe:").pack(pady=5)
        recipe_text = tk.Text(win, width=40)
        recipe_text.insert("1.0", recipe.ingredients)
        recipe_text.pack()
        
        tk.Label(win, text="Rating (0-5):").pack(pady=5)
        rating_entry = tk.Entry(win, width=10)
        rating_entry.insert(0, recipe.rating)
        rating_entry.pack()
        
        def update():
            try:
                new_recipe = Recipe(name=name_entry.get(), recipe=recipe_text.get("1.0", tk.END).strip(), rating=float(rating_entry.get()))
                
                all_recipes = self.recipe_manager.get_all_recipes()
                all_recipes[index] = new_recipe
                self.recipe_manager._recipes = all_recipes
                
                messagebox.showinfo("Success", "Recipe updated!")
                win.destroy()
                parent_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(win, text="Update Recipe", command=update).pack(pady=20)
    
    def show_all(self):
        win = tk.Toplevel(self.root)
        win.title("All Recipes")
        win.geometry("400x400")
        
        tk.Label(win, text=f"Total Recipes: {self.recipe_manager.get_recipe_count()}").pack(pady=10)
        
        text = tk.Text(win, width=45)
        text.pack(pady=10)
        
        all_recipes = self.recipe_manager.get_all_recipes()
        if not all_recipes:
            text.insert("1.0", "No recipes yet.")
        else:
            for recipe in all_recipes:
                text.insert(tk.END, f"• {recipe.name}\n")
                text.insert(tk.END, f"  Difficulty: {recipe.get_difficulty()}\n\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()