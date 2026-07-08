# Próximos Passos — Análise Dívida Ativa

## 1. Perguntas de negócio mais específicas
- [ ] Taxa de inadimplência relativa por UF (cruzar com dado externo de população/PIB, ex. IBGE)
- [x] Concentração de dívida: qual % do valor total está nos maiores devedores (curva de Pareto/Lorenz)
- [ ] Tempo de inscrição em dívida ativa por tipo de devedor (PF vs PJ)

## 2. Ajuizamento como variável de interesse
- [ ] Analisar relação entre ajuizamento e valor da dívida, UF, tipo de devedor
- [ ] Base para uma futura análise preditiva (o que se associa a uma dívida ser ajuizada?)

## 3. Qualidade de dados como narrativa
- [ ] Documentar decisões de tratamento como parte da análise (não só anexo técnico)
- [ ] Reforçar o pipeline de ETL como parte do storytelling do projeto

## 4. Modelagem leve
- [ ] Modelo simples de classificação (scikit-learn) para prever `INDICADOR_AJUIZADO`
- [ ] Usar valor, UF, tipo de devedor como features
- [ ] Reportar métricas mesmo que modestas — mostrar domínio do fluxo preditivo

## 5. Organização e apresentação
- [ ] Consolidar achados em notebook ou README com storytelling (3-4 insights principais)
- [ ] Revisar consistência visual dos gráficos (títulos, formatação de eixo)
- [ ] Investigar dados truncados/incompletos (ex: 2020 e 2026 no gráfico de inscrições por ano)
