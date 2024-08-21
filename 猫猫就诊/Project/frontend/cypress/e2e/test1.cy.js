describe('Test1', () => {
  it('login', () => {
    // 访问网页
    cy.visit('http://101.42.36.160/Main')

    // 选择登录按钮
    cy.contains('登录').click()

    // 输入测试用户名和密码
    cy.contains('身份证号').type('000001')
    // 错误密码测试
    cy.contains('密码').type('12')
    cy.contains('身份选择').click()
    cy.contains('普通用户').click()
    // 正确密码
    cy.contains('密码').type('3456')

    // 点击登录按钮
    cy.contains('登录').click()

    // 进行预约操作
    cy.get('.designed-icon').first().click()
    cy.get('.checkbox-container').click()
    cy.contains('下一步').click()

    cy.contains('首诊').click()
    cy.contains('下一步').click()

    cy.get('input[placeholder="请输入姓名"]').type('小学期可怜人')
    cy.get('select').first().select('医保')
    cy.get('select#gender').select('女')
    cy.get('input#birthday').type('2004-08-18')
    cy.get('select#idType').select('医保卡')
    cy.get('input[placeholder="联系电话"]').type('15308249296')
    cy.get('input[placeholder="请输入证件号"]').type('000001')
    cy.get('input[placeholder="请输入住址"]').type('新北2号机房')
    cy.get('.checkbox-container').click()
    cy.contains('下一步').click()

    cy.contains('皮肤科').click()
    cy.contains('下一步').click()

    cy.contains('有号').click()
    cy.contains('余').click()
    cy.contains('下一步').click()

    cy.contains('10 号').click()
    cy.contains('10 号').click()
    cy.contains('10 号').click()
    cy.contains('下一步').click()

    cy.contains('缴费').click()
    cy.contains('确认缴费').click()
    cy.contains('确认').click()
    cy.contains('确认').click()

    cy.contains('显示详情').click()
    cy.contains('退出').click()

    cy.contains('首页').click()

    // 刷新界面
    cy.reload();

    // // 查看消息
    // cy.contains('消息').click()
    // cy.contains('确认').click()
  })
})
