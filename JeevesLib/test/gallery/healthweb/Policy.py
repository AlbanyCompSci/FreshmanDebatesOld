'''
assume docCanRead: forall (p:prin) (r:record) (s:authstate).
  (In (ActiveRole p Doctor) s) &&
  (In (IsTreating p r.patient) s) &&
  (not (r.subject = Psychiatric)) =>
  GrantedIn (Permit p (Read r.recid)) s

assume psychCanRead: forall (p:prin) (r:record) (s:authstate).
  (In (ActiveRole p Psychiatrist) s) &&
  (In (IsTreating p r.patient) s) &&
  (r.subject = Psychiatric) =>
  GrantedIn (Permit p (Read r.recid)) s

assume patCanConsent: forall (pat:prin) (doc:prin) (s:authstate).
  In (ActiveRole pat Patient) s && In (CanBeInRole doc Doctor) s =>
  GrantedIn (Permit pat (ConsentTo doc)) s

assume pCanActivate: forall (p:prin) (r:role) (s:authstate).
  In (CanBeInRole p r) s => GrantedIn (Permit p (Activate r)) s

assume pCanSearchByKW: forall (p:prin) (s:authstate).
  (In (ActiveRole p Doctor) s ||
   In (ActiveRole p Nurse) s ||
   In (ActiveRole p InsuranceProvider) s) =>
  GrantedIn (Permit p Search) s

assume authorCanRead: forall (p:prin) (r:record) (s:authstate).
  (p=r.author) => GrantedIn (Permit p (Read r.recid)) s

assume patCanRead: forall (p:prin) (r:record) (s:authstate).
  (p=r.patient) && In (ActiveRole p Patient) s =>
  GrantedIn (Permit p (Read r.recid)) s
'''
