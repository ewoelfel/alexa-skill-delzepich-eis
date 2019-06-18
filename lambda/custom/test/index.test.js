let expect = require('chai').expect;
let sinon = require('sinon');
let xray = require('x-ray');
let index = require('../index');
let testData = require('../test_data');

describe('index', function () {

  beforeEach(function(){
    let xrayMock = stub(xray, 'meth').callsFake(function(){
      return testData.html;
    })
  })

  it('should return the correct types for date', function () {

      // given
      let date = new Date(2019, 6, 8)

      // when
      let types = getIcecreamsOfDDate(date);

      // then
      expect(types).to.be.equal(['Schoko','Himbeer - Baiser', 'Schokokuchen', 'Mokka',
                           'Vanille', 'Mascarpone - Blaubeer', 'Milkyway',
                           'Tagessorbet (laktosefrei)']);
  });
});
