import * as React from 'react';
import { Component, Props } from 'react';
import { Panel, Grid, Row, Col, Table } from 'react-bootstrap';
import * as ReactDOM from 'react-dom';

import HeadToHeadChart from './components/head-to-head-chart';
import Stats from './components/head-to-head-stats';
import GoalDistributionChart from './components/goal-distribution-chart';
import NavigationBar from './components/navigation-bar';
import RecentGames from './components/recent-game-list';
import Game from './model/game';
import { getParameters, mostRecentGames } from './utils/utils';


interface HeadToHeadPageProps extends Props<HeadToHeadPage> {
  base: string;
  addURL: string;
  player1: string;
  player2: string;
}
interface HeadToHeadPageState {
  games: Game[];
}
class HeadToHeadPage extends Component<HeadToHeadPageProps, HeadToHeadPageState> {
  constructor(props: HeadToHeadPageProps, context: any) {
    super(props, context);
    this.state = {
      games: undefined,
    };
  }
  async loadGames() {
    const { base, player1, player2 } = this.props;
    const url = `${base}headtohead.cgi?method=games&view=json&player1=${player1}&player2=${player2}`;
    const r = await fetch(url);
    this.setState({games: await r.json()} as HeadToHeadPageState);
  }
  componentDidMount() {
    this.loadGames();
  }
  render() {
    const { base, addURL, player1, player2 } = this.props;
    const { games } = this.state;
    return (
      <div>
        <NavigationBar
          base={base}
          addURL={addURL}
        />
        {games ?
          <Grid fluid={true}>
            <Col md={8}>
              <Stats player1={player1} player2={player2} games={games} base={base}/>
              <Panel>
                <HeadToHeadChart player1={player1} player2={player2} games={games}/>
              </Panel>
            </Col>
            <Col md={4}>
              <Panel header={<h2>Goal Distribution</h2>}>
                <GoalDistributionChart player1={player1} player2={player2} games={games}/>
              </Panel>
              <RecentGames games={mostRecentGames(games)} showAllGames={true} base={base}/>
            </Col>
          </Grid>
          : 'Loading...'
        }
      </div>
    );
  }
}

ReactDOM.render(
  <HeadToHeadPage
    base={'../../../'}
    addURL={'game/add'}
    player1={getParameters(2)[0]}
    player2={getParameters(2)[1]}
  />,
  document.getElementById('entry')
);
