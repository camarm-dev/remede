describe('Page routing checker', () => {
  it('Visits the app root url', () => {
    cy.visit('/dictionnaire')
  })

  it('Visits the bookmark page url', () => {
    cy.visit('/marques-page')
  })

  it('Visits the correction page url', () => {
    cy.visit('/correction')
  })

  it('Visits the sheets page url', () => {
    cy.visit('/fiches')
  })

  it('Visits the settings page url', () => {
    cy.visit('/parametres')
  })

  it('Visits the about page url', () => {
    cy.visit('/a-propos')
  })
})
