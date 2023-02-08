from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField

from wtforms.validators import DataRequired, InputRequired


class SalaireForm(FlaskForm):
    Annee_choix = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
                   '2012','2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021',
                   '2022','2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031']
    Annee = SelectField('Année', choices=Annee_choix, validators=[DataRequired()])
    profession_choix = ["Affaires, finance et administration [1]",
                        "Arts, culture, sports et loisirs [5]",
                        "Cadres intermédiaires dans le commerce de détail, de gros et des services à la clientèle [06]",
                        "Cadres intermédiaires des métiers, des transports, de la production et des services d'utilité publique [07-09]",
                        "Cadres intermédiaires spécialisés/cadres intermédiaires spécialisées [01-05]",
                        "Cadres supérieurs/cadres supérieures [00]",
                        "Dispensateurs/dispensatrices de soins et personnel de soutien en enseignement, en droit et en protection publique [44]",
                        "Enseignement, droit et services sociaux, communautaires et gouvernementaux [4]",
                        "Fabrication et services d'utilité publique [9]",
                        "Gestion [0]",
                        "Manoeuvres dans la transformation, la fabrication et les services d'utilité publique [96]",
                        "Manoeuvres à la récolte, en aménagement paysager et en ressources naturelles [86]",
                        "Monteurs/monteuses dans la fabrication [95]",
                        "Métiers, transport, machinerie et domaines apparentés [7]",
                        "Opérateurs/opératrices de machinerie reliée à la transformation et à la fabrication et autre personnel assimilé [94]",
                        "Personnel d'installation, de réparation et d'entretien et manutentionnaires [74]",
                        "Personnel de coordination de la distribution, du suivi et des horaires [15]",
                        "Personnel de soutien de bureau [14]",
                        "Personnel de soutien des métiers, manoeuvres et aides d'entreprise en construction et autre personnel assimilé [76]",
                        "Personnel de soutien des services de santé [34]",
                        "Personnel de soutien des ventes [66]",
                        "Personnel de soutien en service et autre personnel de service, n.c.a. [67]",
                        "Personnel de supervision dans la transformation, la fabrication et les services d'utilité publique et opérateurs/opératrices de poste central de contrôle [92]",
                        "Personnel de supervision des ventes au détail et personnel des ventes spécialisées [62]",
                        "Personnel de supervision du travail administratif et financier et personnel administratif [12]",
                        "Personnel de supervision en services et personnel de services spécialisés [63]",
                        "Personnel des métiers d'entretien et d'opération d'équipement [73]",
                        "Personnel des métiers de l'électricité, de la construction et des industries [72]",
                        "Personnel des services de protection public de première ligne [43]",
                        "Personnel en finance, assurance et personnel assimilé en administration des affaires [13]",
                        "Personnel en opération d'équipement de transport et de machinerie lourde et autre personnel assimilé à l'entretien [75]",
                        "Personnel en ressources naturelles, en agriculture et en production connexe [84]",
                        "Personnel paraprofessionnel des services juridiques, sociaux, communautaires et de l'enseignement [42]",
                        "Personnel professionnel des arts et de la culture [51]",
                        "Personnel professionnel des sciences naturelles et appliquées [21]",
                        "Personnel professionnel des soins de santé (sauf soins infirmiers) [31]",
                        "Personnel professionnel du droit et des services gouvernementaux, sociaux et communautaires [41]",
                        "Personnel professionnel en gestion des affaires et en finance [11]",
                        "Personnel professionnel en services d'enseignement [40]",
                        "Personnel professionnel en soins infirmiers [30]",
                        "Personnel technique assimilé aux sciences naturelles et appliquées [22]",
                        "Personnel technique des arts, de la culture, des sports et des loisirs [52]",
                        "Personnel technique des soins de santé [32]",
                        "Représentants/représentantes de services et autre personnel de services à la clientèle et personnalisés [65]",
                        "Représentants/représentantes des ventes et vendeurs/vendeuses - commerce de gros et de détail [64]",
                        "Ressources naturelles, agriculture et production connexe [8]",
                        "Sciences naturelles et appliquées et domaines apparentés [2]",
                        "Secteur de la santé [3]",
                        "Superviseurs/superviseures et métiers techniques dans les ressources naturelles,l'agriculture et la production connexe [82]",
                        "Vente et services [6]"
                        ]
    profession = SelectField('Profession (CNP4)', choices=profession_choix, validators=[DataRequired()])

    groupe_choix = ["15 à 24 ans", "25 à 54 ans", "55 ans et plus"]
    groupe = SelectField("Groupe d'âge", choices=groupe_choix, validators=[DataRequired()])

    genre_choix = [(0, 'Femme'), (1, 'Homme')]
    genre = RadioField('Genre', choices=genre_choix, default=1, coerce=int, validators=[InputRequired()])

    type_choix = ["Employés à temps partiel", "Employés à temps plein"]
    type_emploi = SelectField("Type d'emploi", choices=type_choix, validators=[DataRequired()])

    region_choix: list[str] = ['Québec', 'Ontario', 'Colombie-Britannique', 'Manitoba', 'Alberta', 'Saskatchewan',
                               'Nouvelle-Écosse', 'Nouveau-Brunswick', 'Terre-Neuve-et-Labrador',
                               'Île-du-Prince-Édouard']
    region = SelectField('Région', choices=region_choix, validators=[DataRequired()])

    submit = SubmitField("Prédire")
