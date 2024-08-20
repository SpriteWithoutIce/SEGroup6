describe('login test', () => {
  it('login', () => {
    cy.visit('http://101.42.36.160/Main')
    cy.contains('登录').click()
  })
})