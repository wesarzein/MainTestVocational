import streamlit as st

class VocationalTest:
    
    def __init__(self):
        
        self.groups = {
            'g1': ("Ingeniería", ["Ingeniería Ambiental", "Ingeniería Civil", "Ingeniería Industrial", "Ingeniería de Sistemas"]),
            'g2': ("Ciencia de la Salud", ["Medicina", "Enfermería", "Psicología", "Nutrición"]),
            'g3': ("Negocios", ["Administración", "Economía", "Negocios Internacionales"]),
            'g4': ("Arquitectura y Diseño", ["Arquitectura y Urbanismo", "Diseño Industrial"])
        }
        
        self.skills = {
            's1': "Resolución de problemas",
            's2': "Trabajo en equipo",
            's3': "Creatividad",
            's4': "Habilidades comunicativas",
            's5': "Capacidad de análisis",
            's6': "Conocimiento técnico",
            's7': "Atención al detalle"
        }
        
        self.interests = {
            'i1': "Tecnología",
            'i2': "Ciencia",
            'i3': "Arte",
            'i4': "Organización",
            'i5': "Ayudar a otros",
            'i6': "Estudio del comportamiento humano",
            'i7': "Sostenibilidad"
        }
        
        self.activities = {
            'a1': "Proyectos comunitarios",
            'a2': "Ferias de tecnología",
            'a3': "Actividades deportivas",
            'a4': "Voluntariados",
            'a5': "Exposiciones artísticas",
            'a6': "Participación en eventos académicos"
        }
        
        self.selected_area = None
        self.skills_score = {}
        self.interests_score = {}
        self.activities_score = {}

    def get_scores(self):
        st.write("### Selecciona el área de interés:")
        selected_group = None
        for key, (group, _) in self.groups.items():
            if st.checkbox(f"{group}"):
                if selected_group is None:
                    selected_group = key

        if selected_group is None:
            st.warning("Por favor, selecciona el área de interés para continuar.")
            return False
        
        self.selected_area = selected_group

        st.write("### Responde las siguientes preguntas:")

        st.write("#### Habilidades:")
        for key, skill in self.skills.items():
            self.skills_score[key] = st.slider(f"¿Qué tan hábil te consideras en {skill}?", 1, 5)

        st.write("#### Intereses:")
        for key, interest in self.interests.items():
            self.interests_score[key] = st.slider(f"¿Qué tanto te interesa {interest}?", 1, 5)

        st.write("#### Actividades:")
        for key, activity in self.activities.items():
            self.activities_score[key] = st.slider(f"¿En qué medida participas en {activity}?", 1, 5)

        return True

    def get_career(self):
        _, careers_to_evaluate = self.groups[self.selected_area]

        career_matches = {career: 0 for career in self.groups.values() for career in career[1]}

        # requerimientos
        career_requirements = {
            "Ingeniería Ambiental": {'skills': {'s1': 4, 's2': 3, 's6': 4, 's7': 5}, 'interests': {'i7': 5, 'i2': 4}, 'activities': {'a4': 3}},
            "Ingeniería Civil": {'skills': {'s1': 5, 's5': 4, 's6': 5}, 'interests': {'i2': 4}, 'activities': {'a6': 3}},
            "Ingeniería Industrial": {'skills': {'s2': 4, 's5': 4}, 'interests': {'i4': 5}, 'activities': {'a1': 3}},
            "Ingeniería de Sistemas": {'skills': {'s1': 5, 's3': 4, 's6': 5}, 'interests': {'i1': 5, 'i2': 3}, 'activities': {'a2': 4}},
            "Medicina": {'skills': {'s2': 5, 's3': 4, 's4': 5}, 'interests': {'i5': 5, 'i2': 4}, 'activities': {'a4': 5}},
            "Enfermería": {'skills': {'s2': 5, 's3': 4}, 'interests': {'i5': 4}, 'activities': {'a4': 4}},
            "Psicología": {'skills': {'s2': 4, 's3': 5}, 'interests': {'i5': 5, 'i6': 4}, 'activities': {'a1': 3}},
            "Nutrición": {'skills': {'s2': 4, 's3': 3}, 'interests': {'i5': 4}, 'activities': {'a4': 3}},
            "Administración": {'skills': {'s2': 4, 's5': 4}, 'interests': {'i4': 5}, 'activities': {'a1': 3}},
            "Economía": {'skills': {'s5': 5, 's1': 3}, 'interests': {'i4': 4}, 'activities': {'a6': 3}},
            "Negocios Internacionales": {'skills': {'s2': 4, 's5': 4}, 'interests': {'i1': 5}, 'activities': {'a3': 2}},
            "Arquitectura y Urbanismo": {'skills': {'s3': 5, 's7': 5}, 'interests': {'i3': 5, 'i7': 4}, 'activities': {'a5': 4}},
            "Diseño Industrial": {'skills': {'s3': 5, 's4': 4}, 'interests': {'i3': 5}, 'activities': {'a5': 4}}
        }

        # Evaluación de coincidencias
        for career in career_matches.keys():
            requirements = career_requirements.get(career, {})
            for skill_key, required_level in requirements.get('skills', {}).items():
                if self.skills_score.get(skill_key, 0) >= required_level:
                    career_matches[career] += 1
            for interest_key, required_level in requirements.get('interests', {}).items():
                if self.interests_score.get(interest_key, 0) >= required_level:
                    career_matches[career] += 1
            for activity_key, required_level in requirements.get('activities', {}).items():
                if self.activities_score.get(activity_key, 0) >= required_level:
                    career_matches[career] += 1

        recommended_careers = {career: matches for career, matches in career_matches.items() if matches > 0}

        if not recommended_careers:
            return None  

        # carreraxarea
        best_career = max(
            (career for career in recommended_careers.items() if career[0] in careers_to_evaluate),
            key=lambda x: x[1],
            default=None
        )

        if best_career is None:
            return None  
        
        # alternativas
        alternatives = sorted(recommended_careers.items(), key=lambda x: x[1], reverse=True)
        alternatives = [career for career in alternatives if career[0] != best_career[0]]  

        return [best_career] + alternatives[:3]  

    def display_recommendation(self):
        career_result = self.get_career()
        if career_result is None:
            st.write("No se encontró una carrera adecuada basada en tus respuestas.")
            return
        
        best_career = career_result[0]
        
        st.write("### Resultados: ")
        st.markdown(f":star: **Carrera Recomendada:** {best_career[0]}")

        st.write(f" **Carreras alternativas:**")
        for career in career_result[1:]:
            st.write(f"{career[0]}")
            
def main():
    st.title("Testea tu Futuro")
    test = VocationalTest()
    
    if test.get_scores():
        test.display_recommendation()

if __name__ == "__main__":
    main()
