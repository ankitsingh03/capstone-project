import React, { Component } from 'react'
import { connect } from 'react-redux'
import { Route, Switch, Router } from 'react-router-dom'
import PropTypes from 'prop-types'
import history from './history'

import { AdminHome, Main, Checkout, Cart, Home, Login, Signup, UserHome, SingleProduct } from './components'
import { me, fetchProducts, fetchCategories, fetchCart } from './store'


/**
 * COMPONENT
 */
class Routes extends Component {
  componentDidMount() {
    this.props.loadInitialData()
  }

  render() {
    const { isLoggedIn, role } = this.props

    return (
      <Router history={history}>
        <Main>
          <Switch>
            {/* Routes placed here are available to all visitors */}
            <Route exact path="/" component={Home} />
            <Route path="/checkout" component={Checkout} />
            <Route path="/cart" render={() => <Cart container={true} column={true} />} />
            <Route path="/login" component={Login} />
            <Route path="/signup" component={Signup} />
            <Route path="/products/:id" component={SingleProduct} />
            {
              isLoggedIn &&
              <Switch>
                {/* Routes placed here are only available after logging in */}
                {
                  role === 'admin' ?
                    <Route path="/home" component={AdminHome} /> :
                    <Route path="/home" component={UserHome} />
                }
              </Switch>
            }
            {/* Displays our Login component as a fallback */}
            <Route component={Login} />

          </Switch>
        </Main>
      </Router>
    )
  }
}

/**
 * CONTAINER
 */
const mapState = (state) => {
  return {
    // Being 'logged in' for our purposes will be defined has having a state.user that has a truthy id.
    // Otherwise, state.user will be an empty object, and state.user.id will be falsey
    isLoggedIn: !!state.user.id,
    role: state.user.role
  }
}

const mapDispatch = (dispatch) => {
  return {
    loadInitialData() {
      dispatch(me())
      dispatch(fetchProducts())
      dispatch(fetchCategories())
      dispatch(fetchCart())
    }
  }
}

export default connect(mapState, mapDispatch)(Routes)

/**
 * PROP TYPES
 */
Routes.propTypes = {
  loadInitialData: PropTypes.func.isRequired,
  isLoggedIn: PropTypes.bool.isRequired
}
