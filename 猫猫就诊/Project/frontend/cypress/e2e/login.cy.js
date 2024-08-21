describe('login test', () => {
  it('login', () => {
    // 访问网页
    cy.visit('http://101.42.36.160/Main')
    
    // 选择登录按钮
    cy.contains('登录').click()
    
    // 输入测试用户名和密码
    cy.contains('身份证号').type('000001')
    cy.contains('密码').type('123456')
    cy.contains('身份选择').click();
    cy.contains('普通用户').click();

    // 点击登录按钮
    // cy.contains('登录').click();
  })
})
