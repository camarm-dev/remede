describe('Definition page checker', () => {
  it('Visits the \'remède\' definition page', () => {
    cy.visit('/dictionnaire/remède')
  })

  // it('Checks if the word exist (database is responding and parser correctly)', () => {
  //   cy.contains('ion-title .remede-font', 'remède')
  // })
  //
  // it('Checks id the definition is right', () => {
  //   cy.contains('.content ul li span', 'Substance qui sert à guérir un mal ou une maladie')
  // })
})
