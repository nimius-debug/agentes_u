# 1. Agente de Enrutamiento (Routing Agent)

routing_system_prompt = """Eres un Agente de Enrutamiento. Tu función es evaluar la consulta del usuario y dirigirla al departamento relevante. Los departamentos disponibles son:
- Departamento de Investigación de Leads: Maneja tareas relacionadas con la búsqueda de leads en internet.
- Departamento de Generación de Ideas de Negocio: Genera ideas para negocios basadas en contextos o requisitos dados.

Utiliza la herramienta ruta_consulta para enviar la consulta del usuario al departamento relevante. Además, usa la herramienta hablar_con_usuario para obtener más información del usuario si es necesario."""

routing_tools = [
    {
        "type": "function",
        "function": {
            "name": "ruta_consulta",
            "description": "Dirige la consulta del usuario al departamento relevante.",
            "parameters": {
                "type": "object",
                "properties": {
                    "departamento": {
                        "type": "string",
                        "enum": ["Investigación de Leads", "Generación de Ideas de Negocio"],
                        "description": "El departamento al que se dirige la consulta."
                    },
                    "consulta": {
                        "type": "string",
                        "description": "La consulta del usuario a enviar."
                    }
                },
                "required": ["departamento", "consulta"]
            }
        },
        "strict": True
    },
    {
        "type": "function",
        "function": {
            "name": "hablar_con_usuario",
            "description": "Pide más información al usuario.",
            "parameters": {
                "type": "object",
                "properties": {
                    "mensaje": {
                        "type": "string",
                        "description": "El mensaje para enviar al usuario."
                    }
                },
                "required": ["mensaje"]
            }
        },
        "strict": True
    }
]

# 2. Departamento de Investigación de Leads

leads_research_system_prompt = """Formas parte del Departamento de Investigación de Leads. Tu función es manejar tareas relacionadas con la búsqueda de leads en internet. Utiliza la herramienta buscar_leads para realizar tareas de investigación."""

leads_research_tools = [
    {
        "type": "function",
        "function": {
            "name": "buscar_leads",
            "description": "Busca leads en internet basándose en los parámetros dados.",
            "parameters": {
                "type": "object",
                "properties": {
                    "plataforma": {
                        "type": "string",
                        "description": "La plataforma o sitio web donde buscar (ej. Google Maps, LinkedIn, etc.)."
                    },
                    "tipo_negocio": {
                        "type": "string",
                        "description": "El tipo de negocio o industria a buscar."
                    },
                    "ubicacion": {
                        "type": "string",
                        "description": "La ubicación geográfica para la búsqueda."
                    },
                    "criterios_adicionales": {
                        "type": "string",
                        "description": "Cualquier criterio adicional para refinar la búsqueda."
                    }
                },
                "required": ["plataforma", "tipo_negocio", "ubicacion"]
            }
        },
        "strict": True
    }
]

# 3. Departamento de Generación de Ideas de Negocio

idea_generation_system_prompt = """Formas parte del Departamento de Generación de Ideas de Negocio. Tu función es generar ideas innovadoras de negocios basadas en contextos o requisitos dados. Utiliza la herramienta generar_idea_negocio para crear ideas, y la herramienta consultar_conocimiento_negocio para acceder a información relevante del sistema RAG."""

idea_generation_tools = [
    {
        "type": "function",
        "function": {
            "name": "generar_idea_negocio",
            "description": "Genera una idea de negocio basada en los parámetros dados.",
            "parameters": {
                "type": "object",
                "properties": {
                    "industria": {
                        "type": "string",
                        "description": "La industria o sector para la idea de negocio."
                    },
                    "publico_objetivo": {
                        "type": "string",
                        "description": "El público objetivo o base de clientes para el negocio."
                    },
                    "presupuesto": {
                        "type": "string",
                        "description": "El rango de presupuesto aproximado para iniciar el negocio."
                    }
                },
                "required": ["industria", "publico_objetivo", "presupuesto"]
            }
        },
        "strict": True
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_conocimiento_negocio",
            "description": "Consulta el sistema RAG para obtener información relevante sobre negocios.",
            "parameters": {
                "type": "object",
                "properties": {
                    "consulta": {
                        "type": "string",
                        "description": "La consulta para enviar al sistema RAG."
                    }
                },
                "required": ["consulta"]
            }
        },
        "strict": True
    }
]

# Función de ejecución principal

def manejar_consulta_usuario(consulta_usuario):
    # Inicializar conversación
    conversacion = [{"role": "system", "content": routing_system_prompt}]
    conversacion.append({"role": "user", "content": consulta_usuario})

    while True:
        respuesta = client.chat.completions.create(
            model="gpt-4-0613",  # Reemplazar con tu modelo preferido
            messages=conversacion,
            tools=routing_tools,
            tool_choice="auto"
        )

        mensaje_asistente = respuesta.choices[0].message
        conversacion.append(mensaje_asistente)

        if mensaje_asistente.tool_calls:
            for llamada_herramienta in mensaje_asistente.tool_calls:
                if llamada_herramienta.function.name == "ruta_consulta":
                    args = json.loads(llamada_herramienta.function.arguments)
                    departamento = args["departamento"]
                    consulta = args["consulta"]

                    if departamento == "Investigación de Leads":
                        resultado = manejar_departamento_leads(consulta)
                    elif departamento == "Generación de Ideas de Negocio":
                        resultado = manejar_departamento_ideas(consulta)
                    
                    conversacion.append({"role": "function", "name": llamada_herramienta.function.name, "content": resultado})
                
                elif llamada_herramienta.function.name == "hablar_con_usuario":
                    args = json.loads(llamada_herramienta.function.arguments)
                    respuesta_usuario = input(args["mensaje"] + " ")
                    conversacion.append({"role": "user", "content": respuesta_usuario})
        else:
            # Si no hay llamadas a herramientas, asumimos que el asistente tiene una respuesta final
            return mensaje_asistente.content

def manejar_departamento_leads(consulta):
    # Implementar la lógica para el Departamento de Investigación de Leads
    # Esto implicaría usar la herramienta buscar_leads y procesar los resultados
    pass

def manejar_departamento_ideas(consulta):
    # Implementar la lógica para el Departamento de Generación de Ideas de Negocio
    # Esto implicaría usar las herramientas generar_idea_negocio y consultar_conocimiento_negocio
    pass

# Ejemplo de uso
consulta_usuario = "Necesito ideas para una startup tecnológica en el sector educativo"
resultado = manejar_consulta_usuario(consulta_usuario)
print(resultado)